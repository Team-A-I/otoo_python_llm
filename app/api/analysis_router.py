from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from models.models import AnalysisModel, get_analysis_model
from modules.module_analysis import analyze_text

class AnalysisRequest(BaseModel):
    text: str
    type: str  # 'conflict' 또는 'love'

router = APIRouter()

@router.post("/analyze")
async def analyze(request: AnalysisRequest, model: AnalysisModel = Depends(get_analysis_model)):
    try:
        response = analyze_text(model, request.text, request.type)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))