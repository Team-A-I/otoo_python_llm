from fastapi import APIRouter, Depends
from models.models import ChatbotModel, get_chatbot_model
from modules.module_chatbot import ChatbotRequest, generate_chat_response

router = APIRouter()

@router.post("/chatbot")
def chatbot(request: ChatbotRequest, model: ChatbotModel = Depends(get_chatbot_model)):
    response = generate_chat_response(model, request)
    return response