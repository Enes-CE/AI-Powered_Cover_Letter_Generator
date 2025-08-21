from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class ToneType(str, Enum):
    FORMAL = "formal"
    FRIENDLY = "friendly"
    CONCISE = "concise"

class JobPostingRequest(BaseModel):
    """Request model for job posting analysis"""
    job_posting_text: str = Field(..., description="The job posting text to analyze")
    
class CVRequest(BaseModel):
    """Request model for CV/resume data"""
    cv_text: Optional[str] = Field(None, description="CV text in markdown or plain text")
    cv_json: Optional[Dict[str, Any]] = Field(None, description="CV data in JSON format")
    
class CoverLetterRequest(BaseModel):
    """Request model for cover letter generation"""
    job_posting: JobPostingRequest
    cv_data: CVRequest
    tone: ToneType = Field(default=ToneType.FORMAL, description="Tone of the cover letter")
    custom_instructions: Optional[str] = Field(None, description="Custom instructions for generation")

class SkillMatch(BaseModel):
    """Model for skill matching results"""
    skill: str
    matched: bool
    confidence: float
    cv_evidence: Optional[str] = None

class JobAnalysis(BaseModel):
    """Model for job posting analysis results"""
    extracted_skills: List[str]
    required_experience: Optional[str] = None
    company_name: Optional[str] = None
    position_title: Optional[str] = None
    key_requirements: List[str]

class CoverLetterResponse(BaseModel):
    """Response model for generated cover letter"""
    cover_letter: str
    analysis: JobAnalysis
    skill_matches: List[SkillMatch]
    missing_skills: List[str]
    recommendations: List[str]
    tone_used: ToneType

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    service: str
    version: str = "1.0.0"
