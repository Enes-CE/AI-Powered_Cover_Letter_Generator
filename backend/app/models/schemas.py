from pydantic import BaseModel, Field
from typing import List, Optional, Union
from enum import Enum

class ToneType(str, Enum):
    FORMAL = "formal"
    FRIENDLY = "friendly"
    CONCISE = "concise"

class JobPostingRequest(BaseModel):
    job_posting_text: str = Field(..., description="Job posting text content")

class CVRequest(BaseModel):
    cv_text: Optional[str] = Field(None, description="CV text content")
    cv_json: Optional[dict] = Field(None, description="CV data in JSON format")

class CoverLetterRequest(BaseModel):
    job_posting: JobPostingRequest
    cv_data: CVRequest
    company_name: Optional[str] = Field(None, description="Company name for the cover letter")
    position_title: Optional[str] = Field(None, description="Position title for the cover letter")
    years_of_experience: Optional[str] = Field(None, description="Years of experience")
    key_achievements: Optional[str] = Field(None, description="Key achievements and accomplishments")
    tone: ToneType = Field(..., description="Writing tone for the cover letter")
    custom_instructions: Optional[str] = Field(None, description="Custom instructions for generation")
    variants: Optional[int] = Field(1, ge=1, description="Number of cover letter variants to generate")

class ExportRequest(BaseModel):
    cover_letter: str = Field(..., description="Cover letter text content")
    position_title: str = Field("Position", description="Position title")
    company_name: str = Field("Company", description="Company name")

class SkillMatch(BaseModel):
    skill: str
    matched: bool
    confidence: float
    cv_evidence: Optional[str] = None

class JobAnalysis(BaseModel):
    extracted_skills: List[str]
    required_experience: Optional[str] = None
    company_name: Optional[str] = None
    position_title: Optional[str] = None
    key_requirements: List[str] = []

class CoverLetterResponse(BaseModel):
    cover_letter: str
    analysis: JobAnalysis
    skill_matches: List[SkillMatch]
    missing_skills: List[str]
    recommendations: List[str]
    tone_used: ToneType

class CoverLetterBatchResponse(BaseModel):
    letters: List[str]
    analysis: JobAnalysis
    skill_matches: List[SkillMatch]
    missing_skills: List[str]
    recommendations: List[str]
    tone_used: Union[ToneType, List[ToneType]]

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    service: str
    version: str = "1.0.0"
