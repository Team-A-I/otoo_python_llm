from fastapi import HTTPException
from pydantic import BaseModel

class messagesRequest(BaseModel):
    messages: str

async def generate_qna_response(client, messages_request: messagesRequest) -> str:
    return await client.generate_qna_response(messages_request)