from .models import CriterionType, Finding, FindingStatus, Requirement, Segment

def validate_findings(requirements:list[Requirement], findings:list[Finding], segments:list[Segment])->None:
    req_by_id={r.id:r for r in requirements}; segment_by_id={s.segment_id:s for s in segments}
    ids=[f.requirement_id for f in findings]
    if len(ids)!=len(set(ids)): raise ValueError("Duplicate requirement ID")
    if set(ids)!=set(req_by_id): raise ValueError("Missing or unknown requirement ID")
    for finding in findings:
        req=req_by_id[finding.requirement_id]
        if finding.status==FindingStatus.PARTIAL and req.criterion_type not in {CriterionType.DURATION,CriterionType.RUBRIC}: raise ValueError("PARTIAL is limited to duration or confirmed rubric criteria")
        if finding.status in {FindingStatus.MET,FindingStatus.PARTIAL,FindingStatus.CONTRADICTED} and not finding.resume_evidence: raise ValueError("Evidence is required for factual findings")
        if finding.status==FindingStatus.NOT_EVIDENCED and finding.resume_evidence: raise ValueError("NOT_EVIDENCED must not cite fabricated absence evidence")
        for ref in finding.resume_evidence:
            segment=segment_by_id.get(ref.segment_id)
            if not segment: raise ValueError("Unknown segment ID")
            if ref.end_char>len(segment.text) or segment.text[ref.start_char:ref.end_char]!=ref.quote: raise ValueError("Evidence quote or offset does not match stored text")
