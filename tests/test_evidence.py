import pytest
from app.domain.evidence import validate_findings
from app.domain.models import Category, CriterionType, EvidenceRef, Finding, FindingStatus, Requirement, Segment

SEG=Segment(segment_id="s1",source_type="text",text="Built production systems")
REQ=Requirement(id="r1",category=Category.REQUIRED_SKILL,text="systems",criterion_type=CriterionType.BINARY,jd_evidence=[EvidenceRef(segment_id="jd",start_char=0,end_char=1,quote="x")])
def good(): return Finding(requirement_id="r1",status=FindingStatus.MET,reason="evidence",resume_evidence=[EvidenceRef(segment_id="s1",start_char=6,end_char=24,quote="production systems")])
def test_valid_quote(): validate_findings([REQ],[good()],[SEG])
@pytest.mark.parametrize("ref",[EvidenceRef(segment_id="s1",start_char=6,end_char=24,quote="invented quotation"),EvidenceRef(segment_id="s1",start_char=5,end_char=23,quote="production systems")])
def test_invented_or_wrong_offsets_rejected(ref):
    with pytest.raises(ValueError): validate_findings([REQ],[good().model_copy(update={"resume_evidence":[ref]})],[SEG])
def test_duplicate_requirement_rejected():
    with pytest.raises(ValueError): validate_findings([REQ],[good(),good()],[SEG])
def test_unknown_id_rejected():
    with pytest.raises(ValueError): validate_findings([REQ],[good().model_copy(update={"requirement_id":"x"})],[SEG])
def test_not_evidenced_cannot_have_quote():
    with pytest.raises(ValueError): validate_findings([REQ],[good().model_copy(update={"status":FindingStatus.NOT_EVIDENCED})],[SEG])
