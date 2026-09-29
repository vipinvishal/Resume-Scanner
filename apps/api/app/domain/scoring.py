from decimal import Decimal, ROUND_HALF_UP
from .models import Category, CategoryResult, Finding, FindingStatus, Requirement, ScoreResult

WEIGHTS={Category.REQUIRED_SKILL:35,Category.EXPERIENCE:25,Category.RESPONSIBILITY:20,Category.PREFERRED_SKILL:15,Category.EDUCATION_CERTIFICATION:5}
CREDIT={FindingStatus.MET:Decimal("1"),FindingStatus.PARTIAL:Decimal("0.5"),FindingStatus.NOT_EVIDENCED:Decimal("0"),FindingStatus.CONTRADICTED:Decimal("0")}

def half_up(value:Decimal)->int: return int(value.quantize(Decimal("1"),rounding=ROUND_HALF_UP))

def score(requirements:list[Requirement], findings:list[Finding])->ScoreResult:
    if not requirements: return ScoreResult(score=None,coverage=None,exact_score=None,exact_coverage=None,active_weight=0,categories=[],reason="NO_CRITERIA")
    by_id={f.requirement_id:f for f in findings}
    if len(by_id)!=len(findings): raise ValueError("Duplicate requirement IDs")
    required={r.id for r in requirements}
    if set(by_id)!=required:
        missing=required-set(by_id); extra=set(by_id)-required
        raise ValueError(f"Finding IDs mismatch; missing={sorted(missing)}, extra={sorted(extra)}")
    total=Decimal(0); covered=Decimal(0); active_weight=0; categories=[]
    for category,weight in WEIGHTS.items():
        reqs=[r for r in requirements if r.category==category]
        if not reqs: continue
        active_weight+=weight
        category_credit=sum((CREDIT[by_id[r.id].status] for r in reqs),Decimal(0))/len(reqs)
        category_coverage=sum((Decimal(0) if by_id[r.id].status==FindingStatus.NOT_EVIDENCED else Decimal(1) for r in reqs),Decimal(0))/len(reqs)
        contribution=Decimal(weight)*category_credit; total+=contribution; covered+=Decimal(weight)*category_coverage
        categories.append(CategoryResult(category=category,base_weight=weight,criterion_count=len(reqs),credit=str(category_credit),contribution=str(contribution)))
    exact=Decimal(100)*total/Decimal(active_weight); exact_coverage=Decimal(100)*covered/Decimal(active_weight)
    return ScoreResult(score=half_up(exact),coverage=half_up(exact_coverage),exact_score=str(exact),exact_coverage=str(exact_coverage),active_weight=active_weight,categories=categories)
