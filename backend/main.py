from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.cover_letter import router as cover_letter_router
import uvicorn

app = FastAPI(
    title="AI Cover Letter Generator API",
    description="An intelligent API for generating personalized cover letters",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(cover_letter_router, prefix="/api", tags=["cover-letter"])

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AI Cover Letter Generator API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "cover-letter-generator"}

@app.get("/api/status")
async def api_status():
    """API status endpoint"""
    return {
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "generate": "/api/generate-cover-letter",
            "analyze": "/api/analyze-job-posting"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
