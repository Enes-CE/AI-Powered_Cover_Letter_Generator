from fastapi import APIRouter, HTTPException
from app.models.schemas import CoverLetterRequest, CoverLetterResponse, JobAnalysis, SkillMatch, ToneType
from typing import List

router = APIRouter()

@router.post("/generate-cover-letter", response_model=CoverLetterResponse)
async def generate_cover_letter(request: CoverLetterRequest):
    """
    Generate a personalized cover letter based on job posting and CV
    """
    try:
        # TODO: Implement actual AI generation
        # For now, return a mock response
        
        # Mock analysis
        analysis = JobAnalysis(
            extracted_skills=["Python", "FastAPI", "React", "Machine Learning"],
            required_experience="3+ years",
            company_name="Tech Corp",
            position_title="Senior Software Engineer",
            key_requirements=["Python", "API Development", "Frontend", "AI/ML"]
        )
        
        # Mock skill matches
        skill_matches = [
            SkillMatch(skill="Python", matched=True, confidence=0.9, cv_evidence="3 years experience"),
            SkillMatch(skill="FastAPI", matched=True, confidence=0.8, cv_evidence="Built REST APIs"),
            SkillMatch(skill="React", matched=True, confidence=0.7, cv_evidence="Frontend development"),
            SkillMatch(skill="Machine Learning", matched=False, confidence=0.3, cv_evidence="Basic knowledge")
        ]
        
        # Mock cover letter
        cover_letter = f"""
Dear Hiring Manager,

I am writing to express my strong interest in the {analysis.position_title} position at {analysis.company_name}. With my background in software development and experience with Python, FastAPI, and React, I believe I would be a valuable addition to your team.

My experience includes:
- 3+ years of Python development
- Building REST APIs with FastAPI
- Frontend development with React
- Basic knowledge of Machine Learning

I am excited about the opportunity to contribute to your innovative projects and grow with your team.

Best regards,
[Your Name]
        """.strip()
        
        return CoverLetterResponse(
            cover_letter=cover_letter,
            analysis=analysis,
            skill_matches=skill_matches,
            missing_skills=["Advanced Machine Learning", "Docker"],
            recommendations=[
                "Highlight your Python experience more prominently",
                "Consider learning Docker for containerization",
                "Take an advanced ML course to strengthen your profile"
            ],
            tone_used=request.tone
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating cover letter: {str(e)}")

@router.get("/test")
async def test_endpoint():
    """Test endpoint to verify API is working"""
    return {"message": "Cover letter API is working!", "status": "success"}
