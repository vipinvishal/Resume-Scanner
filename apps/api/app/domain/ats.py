from decimal import Decimal
from .models import AtsCheck, AtsResult
from .scoring import half_up

def calculate_ats(checks:list[AtsCheck])->AtsResult:
    assessed=sum(c.weight for c in checks if c.result!="unassessed")
    blocks=any(c.name in {"text_availability","character_integrity"} and c.result=="fail" for c in checks)
    if assessed<80: return AtsResult(score=None,assessed_weight=assessed,label="Insufficient format assessment",checks=checks,blocks_match=blocks)
    earned=sum(c.weight for c in checks if c.result=="pass")
    value=half_up(Decimal(100)*Decimal(earned)/Decimal(assessed))
    return AtsResult(score=value,assessed_weight=assessed,label="ATS readiness",checks=checks,blocks_match=blocks)
