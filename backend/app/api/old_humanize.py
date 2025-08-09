from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional
import os
from app.services.humanizer import humanizer

router = APIRouter()

class HumanizeRequest(BaseModel):
    text: str

class HumanizeResponse(BaseModel):
    original_text: str
    humanized_text: str
    processing_time_ms: int
    ai_detection_score_before: float
    ai_detection_score_after: float
    readability_improvement: float

@router.post("/text", response_model=HumanizeResponse)
async def humanize_text(request: HumanizeRequest):
    """
    Humanize AI-generated text
    
    Example:
    {
        "text": "The artificial intelligence system demonstrates remarkable capabilities in natural language processing."
    }
    """
    # Validate input
    is_valid, error_message = humanizer.validate_input(request.text)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)
    
    try:
        # Process the text
        result = humanizer.humanize_text(request.text)
        
        return HumanizeResponse(
            original_text=result["original_text"],
            humanized_text=result["humanized_text"],
            processing_time_ms=result["processing_time_ms"],
            ai_detection_score_before=result["ai_detection_score_before"],
            ai_detection_score_after=result["ai_detection_score_after"],
            readability_improvement=result["readability_improvement"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

@router.post("/file")
async def humanize_file(file: UploadFile = File(...)):
    """
    Humanize text from uploaded file
    
    Supports: .txt files (up to 5MB)
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
        
        # Process the text
        result = humanizer.humanize_text(text)
        
        return {
            "filename": file.filename,
            "original_text": result["original_text"],
            "humanized_text": result["humanized_text"],
            "processing_time_ms": result["processing_time_ms"],
            "ai_detection_score_before": result["ai_detection_score_before"],
            "ai_detection_score_after": result["ai_detection_score_after"],
            "readability_improvement": result["readability_improvement"]
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
        "version": "1.0.0",
        "features": [
            "text_humanization",
            "file_upload",
            "ai_detection_scoring",
            "readability_analysis"
        ]
    }

@router.get("/demo")
async def demo():
    """
    Demo endpoint with sample humanization
    """
    sample_text = "The artificial intelligence system demonstrates remarkable capabilities in natural language processing and text generation."
    
    try:
        result = humanizer.humanize_text(sample_text)
        
        return {
            "demo": True,
            "sample_input": sample_text,
            "result": result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in demo: {str(e)}") 