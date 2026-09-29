from __future__ import annotations
from datetime import date
from enum import StrEnum
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator

class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

class Category(StrEnum):
    REQUIRED_SKILL="required_skill"; EXPERIENCE="experience"; RESPONSIBILITY="responsibility"; PREFERRED_SKILL="preferred_skill"; EDUCATION_CERTIFICATION="education_certification"
class CriterionType(StrEnum): BINARY="binary"; DURATION="duration"; RUBRIC="rubric"
class FindingStatus(StrEnum): MET="MET"; PARTIAL="PARTIAL"; NOT_EVIDENCED="NOT_EVIDENCED"; CONTRADICTED="CONTRADICTED"

class Segment(StrictModel):
    segment_id:str; source_type:Literal["pdf","docx","text"]; text:str; page:int|None=None; paragraph_index:int|None=None; table_cell:str|None=None
class EvidenceRef(StrictModel):
    segment_id:str; start_char:int=Field(ge=0); end_char:int=Field(ge=1); quote:str
    @model_validator(mode="after")
    def valid_span(self):
        if self.end_char <= self.start_char: raise ValueError("Evidence end offset must follow start offset")
        return self
class Requirement(StrictModel):
    id:str; category:Category; text:str; criterion_type:CriterionType=CriterionType.BINARY; min_months:int|None=Field(default=None,ge=1); essential:bool=False; origin:Literal["jd","recruiter"]="jd"; jd_evidence:list[EvidenceRef]=[]; recruiter_reason:str|None=None; rubric_partial:str|None=None; rubric_full:str|None=None
    @model_validator(mode="after")
    def valid_origin(self):
        if self.origin=="jd" and not self.jd_evidence: raise ValueError("JD criteria require evidence")
        if self.origin=="recruiter" and not self.recruiter_reason: raise ValueError("Recruiter criteria require a reason")
        if self.criterion_type==CriterionType.RUBRIC and not (self.rubric_partial and self.rubric_full): raise ValueError("Rubrics require full and partial conditions")
        return self
class RelevantInterval(StrictModel):
    start:str; end:str; evidence:list[EvidenceRef]=[]
class Finding(StrictModel):
    requirement_id:str; status:FindingStatus; reason:str; resume_evidence:list[EvidenceRef]=[]; relevant_intervals:list[RelevantInterval]=[]; question:str|None=None
class EvaluationOutput(StrictModel): findings:list[Finding]
class JDExtractionOutput(StrictModel): requirements:list[Requirement]
class CategoryResult(StrictModel): category:Category; base_weight:int; criterion_count:int; credit:str; contribution:str
class ScoreResult(StrictModel):
    score:int|None; coverage:int|None; exact_score:str|None; exact_coverage:str|None; active_weight:int; categories:list[CategoryResult]; reason:str|None=None
class AtsCheck(StrictModel): name:str; weight:int; result:Literal["pass","fail","unassessed"]; observed:str
class AtsResult(StrictModel): score:int|None; assessed_weight:int; label:str; checks:list[AtsCheck]; blocks_match:bool=False
class DecisionInput(StrictModel):
    status:Literal["shortlisted","talk_first","rejected"]; note:str=Field(min_length=5,max_length=2000); questions:list[str]=[]; analysis_id:str; expected_version:int=Field(ge=0)
    @model_validator(mode="after")
    def talk_needs_question(self):
        if self.status=="talk_first" and not any(10<=len(q)<=500 for q in self.questions): raise ValueError("Talk to Candidate requires a question of 10 to 500 characters")
        return self
