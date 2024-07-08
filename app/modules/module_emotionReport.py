from pydantic import BaseModel

class EmotionReportRequest(BaseModel):
    text: str

def generate_messages_response(client, request: EmotionReportRequest) -> str:
    return client.generate_messages_response(request.text)