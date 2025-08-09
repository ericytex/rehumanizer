from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional
import os
from app.services.humanizer import humanizer

router = APIRouter()

class HumanizeRequest(BaseModel):
    text: str
    pipeline_type: str = "comprehensive"
    education_level: str = "undergraduate"  # elementary, middle_school, high_school, undergraduate, masters, phd
    paranoid_mode: bool = True  # Extra aggressive coherence disruption for GPTZero & SurferSEO
    writehuman_mode: bool = True  # WriteHuman mimicry for SurferSEO final strike

class HumanizeResponse(BaseModel):
    original_text: str
    paraphrased_text: str
    humanized_text: str
    processing_time_ms: int
    ai_detection_score_before: float
    ai_detection_score_after: float
    readability_improvement: float
    education_level: Optional[str] = None
    gemini_humanized_text: Optional[str] = None
    meaning_preserved: Optional[bool] = None

@router.post("/text", response_model=HumanizeResponse)
async def humanize_text(request: HumanizeRequest):
    """
    Humanize AI-generated text with advanced algorithms and educational level customization
    
    Example:
    {
        "text": "The artificial intelligence system demonstrates remarkable capabilities in natural language processing.",
        "pipeline_type": "comprehensive",
        "education_level": "undergraduate",
        "paranoid_mode": true,
        "writehuman_mode": true
    }
    
    Education Levels: elementary, middle_school, high_school, undergraduate, masters, phd
    Pipeline Types: comprehensive, standard, quick, advanced
    Paranoid Mode: Extra aggressive coherence disruption for GPTZero & SurferSEO evasion
    WriteHuman Mode: Mimics WriteHuman.ai's approach to reduce SurferSEO detection from 52% to <20%
    """
    # Validate input
    is_valid, error_message = humanizer.validate_input(request.text)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)
    
    try:
        # Process the text with new parameters
        result = humanizer.humanize_text(
            request.text, 
            request.pipeline_type, 
            request.education_level,
            request.paranoid_mode,
            request.writehuman_mode
        )
        
        return HumanizeResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

@router.post("/file")
async def humanize_file(
    file: UploadFile = File(...), 
    pipeline_type: str = "comprehensive",
    education_level: str = "undergraduate",
    paranoid_mode: bool = True,
    writehuman_mode: bool = True
):
    """
    Humanize text from uploaded file with advanced algorithms
    
    Supports: .txt files (up to 5MB)
    Education Levels: elementary, middle_school, high_school, undergraduate, masters, phd
    Pipeline Types: comprehensive, standard, quick, advanced
    Paranoid Mode: Extra aggressive coherence disruption for GPTZero & SurferSEO evasion
    WriteHuman Mode: Mimics WriteHuman.ai's approach to reduce SurferSEO detection from 52% to <20%
    """
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Check file size (5MB limit)
    max_size = 5 * 1024 * 1024
    if file.size and file.size > max_size:
        raise HTTPException(
            status_code=400, 
            detail=f"File size exceeds maximum allowed size of 5MB"
        )
    
    # Check file type
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension != '.txt':
        raise HTTPException(
            status_code=400,
            detail="Only .txt files are supported for MVP"
        )
    
    try:
        # Read file content
        content = await file.read()
        text = content.decode('utf-8')
        
        # Validate text content
        is_valid, error_message = humanizer.validate_input(text)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_message)
        
        # Process the text with new parameters
        result = humanizer.humanize_text(text, pipeline_type, education_level, paranoid_mode, writehuman_mode)
        
        return {
            "filename": file.filename,
            **result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.get("/health")
async def health_check():
    """
    Health check endpoint for humanization service
    """
    return {
        "status": "healthy",
        "service": "humanizer",
        "version": "7.0.0",
        "features": [
            "text_humanization",
            "file_upload",
            "ai_detection_scoring",
            "readability_analysis",
            "stylometric_masking",
            "pegasus_paraphrasing",
            "gemini_humanization",
            "multi_detector_evasion",
            "educational_level_adjustment",
            "perplexity_optimization",
            "comprehensive_pipeline",
            "meaning_preservation",
            "coherence_disruption",
            "gptzero_evasion",
            "surferseo_evasion"
        ],
        "education_levels": [
            "elementary",
            "middle_school", 
            "high_school",
            "undergraduate",
            "masters",
            "phd"
        ],
        "pipeline_types": [
            "comprehensive",
            "standard", 
            "quick",
            "advanced"
        ]
    }

@router.get("/demo")
async def demo():
    """
    Demo endpoint with sample humanization using comprehensive pipeline
    """
    sample_text = "The artificial intelligence system demonstrates remarkable capabilities in natural language processing and text generation."
    
    try:
        result = humanizer.humanize_text(sample_text, "comprehensive", "undergraduate", True, True)
        
        return {
            "demo": True,
            "sample_input": sample_text,
            "pipeline_used": "comprehensive",
            "education_level": "undergraduate",
            "result": result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in demo: {str(e)}")
