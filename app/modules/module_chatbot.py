from pydantic import BaseModel
from typing import List

class ChatbotRequest(BaseModel):
    mode: str
    recent_messages: List[str]

def generate_chat_response(client, request: ChatbotRequest) -> str:
    return client.generate_chat_response(request.mode, request.recent_messages)