from fastapi import APIRouter, Depends
from models.models import EmotionReportModel, get_emotion_report_model
from modules.module_emotionReport import EmotionReportRequest, generate_messages_response

router = APIRouter()

@router.post("/emotionReport")
def emotion_report(request: EmotionReportRequest, model: EmotionReportModel = Depends(get_emotion_report_model)):
    response = generate_messages_response(model, request)
    return response