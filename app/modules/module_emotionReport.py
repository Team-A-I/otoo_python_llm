from fastapi import HTTPException
from pydantic import BaseModel

class messagesRequest(BaseModel):
    messages: str

def generate_messages_response(client, messages_request: messagesRequest) -> str:
    return client.generate_messages_response(messages_request)