from functools import lru_cache
from pathlib import Path
from typing import Literal
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

FREE_TIER_MODEL = "gemini-3.5-flash-lite"

class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file=Path(__file__).resolve().parents[1] / ".env",extra="ignore")
    ai_mode:Literal["demo","live"]="demo"
    supabase_url:str=""; supabase_public_key:str=""; supabase_service_key:str=""; gemini_api_key:str=""
    # Customer-required guard: no paid Google model can be selected.
    model_id:str=FREE_TIER_MODEL; gemini_input_usd_per_million:float=0; gemini_output_usd_per_million:float=0
    monthly_budget_usd:float=10; allowed_origins:str="http://localhost:5173"; worker_concurrency:int=Field(2,ge=1,le=2)
    @model_validator(mode="after")
    def live_requires_credentials(self):
        if self.model_id != FREE_TIER_MODEL:
            raise ValueError(f"This application permits only the free-tier model {FREE_TIER_MODEL}")
        if self.ai_mode=="live":
            missing=[k for k in ("supabase_url","supabase_public_key","supabase_service_key","gemini_api_key") if not getattr(self,k)]
            if missing: raise ValueError(f"Live mode configuration missing: {', '.join(missing)}")
        return self
@lru_cache
def get_settings(): return Settings()
