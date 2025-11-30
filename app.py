# app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rewrite_api import rewrite_text
from plagiarism_check import check_plagiarism
from ai_detect import detect_ai

app = FastAPI(title="RoRoWrites HumanAizer API")

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class TextInput(BaseModel):
    text: str
    style: str = None

class PlagiarismInput(BaseModel):
    text: str
    reference_text: str = None

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "RoRoWrites HumanAizer API",
        "status": "active",
        "endpoints": ["/rewrite", "/plagiarism", "/ai_detect", "/generate"]
    }

# Rewrite endpoint
@app.post("/rewrite")
def rewrite(input_data: TextInput):
    try:
        if not input_data.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        rewritten = rewrite_text(input_data.text, input_data.style)
        return {"rewritten_text": rewritten}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Plagiarism check endpoint
@app.post("/plagiarism")
def plagiarism(input_data: PlagiarismInput):
    try:
        if not input_data.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        result = check_plagiarism(input_data.text, input_data.reference_text)
        return {"plagiarism_result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# AI detection endpoint
@app.post("/ai_detect")
def ai_detect_endpoint(input_data: TextInput):
    try:
        if not input_data.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        result = detect_ai(input_data.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Generate unique content endpoint
@app.post("/generate")
def generate(input_data: TextInput):
    try:
        if not input_data.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Use rewrite_text with creative style
        generated = rewrite_text(input_data.text, style="creative")
        return {"generated_unique_text": generated}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}