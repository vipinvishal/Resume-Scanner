import pytest
from pydantic import ValidationError
from app.config import FREE_TIER_MODEL, Settings

def test_free_tier_model_is_default_and_only_allowed_model():
    assert Settings().model_id == FREE_TIER_MODEL
    with pytest.raises(ValidationError, match="permits only the free-tier model"):
        Settings(model_id="gemini-3.8-flash")
