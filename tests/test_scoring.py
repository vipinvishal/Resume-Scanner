from decimal import Decimal
from app.domain.models import Category, CriterionType, EvidenceRef, Finding, FindingStatus, Requirement
from app.domain.scoring import score

def req(id,category): return Requirement(id=id,category=category,text=id,criterion_type=CriterionType.BINARY,jd_evidence=[EvidenceRef(segment_id="jd",start_char=0,end_char=1,quote="x")])
def finding(id,status): return Finding(requirement_id=id,status=status,reason="test",resume_evidence=[] if status==FindingStatus.NOT_EVIDENCED else [EvidenceRef(segment_id="r",start_char=0,end_char=1,quote="x")])

def test_lld_worked_example_is_70():
    requirements=[]; findings=[]
    for i,status in enumerate([FindingStatus.MET,FindingStatus.MET,FindingStatus.MET,FindingStatus.NOT_EVIDENCED]): requirements.append(req(f"s{i}",Category.REQUIRED_SKILL)); findings.append(finding(f"s{i}",status))
    for i,status in enumerate([FindingStatus.MET,FindingStatus.NOT_EVIDENCED]): requirements.append(req(f"e{i}",Category.EXPERIENCE)); findings.append(finding(f"e{i}",status))
    requirements.append(req("r",Category.RESPONSIBILITY)); findings.append(finding("r",FindingStatus.MET))
    requirements.extend([req("p1",Category.PREFERRED_SKILL),req("p2",Category.PREFERRED_SKILL)]); findings.extend([finding("p1",FindingStatus.MET),finding("p2",FindingStatus.NOT_EVIDENCED)])
    result=score(requirements,findings)
    assert result.score==70
    assert result.active_weight==95
def test_absent_categories_normalize():
    result=score([req("r",Category.REQUIRED_SKILL)],[finding("r",FindingStatus.MET)])
    assert result.score==100
def test_missing_evidence_remains_denominator():
    result=score([req("a",Category.REQUIRED_SKILL),req("b",Category.REQUIRED_SKILL)],[finding("a",FindingStatus.MET),finding("b",FindingStatus.NOT_EVIDENCED)])
    assert result.score==50 and result.coverage==50
def test_no_criteria_returns_null(): assert score([],[]).score is None
def test_ats_does_not_enter_job_match():
    baseline=score([req("r",Category.REQUIRED_SKILL)],[finding("r",FindingStatus.MET)])
    assert baseline.score==100
