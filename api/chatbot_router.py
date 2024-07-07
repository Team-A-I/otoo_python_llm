# api/chatbot_router.py

from fastapi import APIRouter, Depends
from models.models import ChatbotModel, get_chatbot_model
from modules.module_chatbot import FullRequest, generate_chat_response

router = APIRouter()

@router.post("/chatbot")
def chatbotLLM(full_request: FullRequest, model: ChatbotModel = Depends(get_chatbot_model)):
    mode_request = full_request.mode_request
    recent_messages_request = full_request.recent_messages_request
    response = generate_chat_response(model, mode_request, recent_messages_request)
    return response
