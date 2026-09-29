from __future__ import annotations
import re
from datetime import date
from pathlib import Path
from fastapi import HTTPException, UploadFile
from ..adapters.documents import DocumentError, parse_docx, parse_pdf, redact_segments
from ..adapters.provider import GeminiProvider
from ..config import Settings
from ..domain.ats import calculate_ats
from ..domain.evidence import validate_findings
from ..domain.models import AtsCheck, EvidenceRef, Segment
from ..domain.scoring import score

def _text_segment(text:str)->Segment:
    normalized=re.sub(r"\s+"," ",text).strip()
    if len(normalized)<50: raise HTTPException(422,"Paste a job description with at least 50 characters")
    if len(normalized)>60_000: raise HTTPException(422,"Job description exceeds 60,000 characters")
    return Segment(segment_id="jd-1",source_type="text",text=normalized)

def _recompute_offsets(segments:list[Segment],refs:list[EvidenceRef])->list[EvidenceRef]:
    # The model is asked for exact code-point offsets alongside each quote, but a
    # lite model frequently miscounts them even when the quote text itself is a
    # genuine, verbatim substring. Recompute offsets from the quote's real
    # position in the source text; a quote that cannot be located at all is left
    # untouched so the downstream exact-match check still rejects it as invented.
    by_id={segment.segment_id:segment for segment in segments}
    corrected=[]
    for ref in refs:
        segment=by_id.get(ref.segment_id)
        index=segment.text.find(ref.quote) if segment else -1
        corrected.append(ref if index==-1 else ref.model_copy(update={"start_char":index,"end_char":index+len(ref.quote)}))
    return corrected

def _validate_refs(segments:list[Segment],refs):
    by_id={segment.segment_id:segment for segment in segments}
    for ref in refs:
        segment=by_id.get(ref.segment_id)
        if not segment or ref.end_char>len(segment.text) or segment.text[ref.start_char:ref.end_char]!=ref.quote:
            raise ValueError("Model returned an invalid job-description quote")

def _ats(segments:list[Segment]):
    text="\n".join(s.text for s in segments); nonspace=len(re.sub(r"\s","",text)); invalid=len(re.findall(r"\ufffd|[\x00-\x08\x0b\x0c\x0e-\x1f]",text))
    headings=sum(bool(re.search(rf"\b{name}\b",text,re.I)) for name in ("skills","experience","education","projects","certifications"))
    month_range=bool(re.search(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}\s*[-–]\s*(?:Present|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4})",text,re.I))
    checks=[AtsCheck(name="text_availability",weight=35,result="pass" if nonspace>=200 else "fail",observed=f"{nonspace} non-whitespace characters"),AtsCheck(name="character_integrity",weight=20,result="pass" if not text or invalid/len(text)<.01 else "fail",observed=f"{invalid} invalid characters"),AtsCheck(name="reading_order",weight=20,result="unassessed",observed="Geometry is not retained by the local parser"),AtsCheck(name="section_structure",weight=15,result="pass" if headings>=2 else "fail",observed=f"{headings} known section headings"),AtsCheck(name="date_readability",weight=10,result="pass" if month_range else "unassessed",observed="Month-year range found" if month_range else "No reliable month-year range")]
    return calculate_ats(checks)

async def analyze_live(resume:UploadFile,jd_text:str,candidate_name:str|None,settings:Settings)->dict:
    if settings.ai_mode!="live": raise HTTPException(409,"Live analysis is disabled. Set AI_MODE=live in apps/api/.env and restart the API.")
    filename=resume.filename or "resume"
    try:
        data=await resume.read()
        parsed=parse_pdf(data) if filename.lower().endswith(".pdf") else parse_docx(data) if filename.lower().endswith(".docx") else (_ for _ in ()).throw(DocumentError("Only PDF and DOCX resumes are supported"))
    except DocumentError as exc: raise HTTPException(422,str(exc)) from exc
    redacted,warnings=redact_segments(parsed.segments,candidate_name)
    jd_segment=_text_segment(jd_text); provider=GeminiProvider(settings)
    try:
        extraction=provider.extract_requirements([jd_segment])
        if not extraction.requirements: raise ValueError("No explicit job requirements were found")
        extraction=extraction.model_copy(update={"requirements":[r.model_copy(update={"jd_evidence":_recompute_offsets([jd_segment],r.jd_evidence)}) for r in extraction.requirements]})
        for requirement in extraction.requirements: _validate_refs([jd_segment],requirement.jd_evidence)
        evaluation=provider.evaluate(extraction.requirements,redacted)
        evaluation=evaluation.model_copy(update={"findings":[f.model_copy(update={"resume_evidence":_recompute_offsets(redacted,f.resume_evidence)}) for f in evaluation.findings]})
        validate_findings(extraction.requirements,evaluation.findings,redacted)
    except ValueError as exc: raise HTTPException(422,f"Analysis validation failed: {exc}") from exc
    except Exception as exc: raise HTTPException(502,"Gemini analysis failed. Check your key, free-tier quota, and retry.") from exc
    match=score(extraction.requirements,evaluation.findings); ats=_ats(redacted)
    score_value=None if ats.blocks_match else match.score
    questions=[f.question for f in evaluation.findings if f.question]
    return {"analysis_id":"local-live-analysis","status":"ready","stage":"Ready","report":{"schema_version":"report_v1","candidate_code":"LOCAL-REVIEW","job_title":"Live job description","job_match":score_value,"evidence_coverage":match.coverage,"ats_readiness":ats.score,"coverage_notice":bool(match.coverage is not None and match.coverage<60),"findings":[{"requirement_id":f.requirement_id,"requirement":next(r.text for r in extraction.requirements if r.id==f.requirement_id),"category":next(r.category.value for r in extraction.requirements if r.id==f.requirement_id),"status":f.status.value,"reason":f.reason,"quote":f.resume_evidence[0].quote if f.resume_evidence else None,"source":f.resume_evidence[0].segment_id if f.resume_evidence else None} for f in evaluation.findings],"questions":questions,"category_contributions":[c.model_dump() for c in match.categories],"ats_checks":[c.model_dump() for c in ats.checks],"redaction_warnings":warnings,"versions":{"model":settings.model_id,"scoring":"job_match_v1","ats":"ats_readiness_v1","prompt":"resume_eval_v1","redaction":"redact_v1"},"evaluation_as_of":date.today().isoformat()}}
