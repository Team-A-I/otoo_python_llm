from fastapi import FastAPI
from openai import OpenAI
from dotenv import load_dotenv
from module_chatbot import generate_chat_response, FullRequest
from module_emotionReport import generate_messages_response, messagesRequest
import os
from typing import List

app = FastAPI()
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

@app.get("/llm-endpoint")
def read_fastapi():
    return {"message": "Hello from llm"}


@app.post("/emotionReport")
async def emotionReportLLM(messages_request: messagesRequest):
    response = generate_messages_response(client, messages_request)
    return response



@app.post("/chatbot")
async def chatbotLLM(full_request: FullRequest):
    mode_request = full_request.mode_request
    recent_messages_request = full_request.recent_messages_request
    response = generate_chat_response(client, mode_request, recent_messages_request)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

# uvicorn main:app --reload --port 8001