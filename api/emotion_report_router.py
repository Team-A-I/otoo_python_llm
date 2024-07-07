# api/emotion_report_router.py

from fastapi import APIRouter, Depends
from models.models import EmotionReportModel, get_emotion_report_model
from modules.module_emotionReport import messagesRequest, generate_messages_response

router = APIRouter()

@router.post("/emotionReport")
async def emotionReportLLM(messages_request: messagesRequest, model: EmotionReportModel = Depends(get_emotion_report_model)):
    response = generate_messages_response(model, messages_request)
    return response
