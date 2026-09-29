from datetime import date
import pytest
from app.domain.duration import merged_months
from app.domain.ats import calculate_ats
from app.domain.models import AtsCheck
def test_overlap_is_merged(): assert merged_months([("2024-01","2024-06"),("2024-04","2024-09")],date(2026,9,29))==8
def test_present_uses_evaluation_date(): assert merged_months([("2026-01","Present")],date(2026,9,29))==9
def test_year_only_rejected():
    with pytest.raises(ValueError): merged_months([("2024","2025")],date(2026,9,29))
def test_ats_needs_80_assessed_weight():
    out=calculate_ats([AtsCheck(name="text_availability",weight=35,result="pass",observed="ok"),AtsCheck(name="character_integrity",weight=20,result="pass",observed="ok")])
    assert out.score is None and out.label=="Insufficient format assessment"
def test_failed_text_blocks_match():
    out=calculate_ats([AtsCheck(name="text_availability",weight=35,result="fail",observed="scan"),AtsCheck(name="character_integrity",weight=20,result="pass",observed="ok"),AtsCheck(name="reading_order",weight=20,result="pass",observed="ok"),AtsCheck(name="section_structure",weight=15,result="pass",observed="ok")])
    assert out.blocks_match
