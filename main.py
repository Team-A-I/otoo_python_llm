from openai import OpenAI
from dotenv import load_dotenv
from module_chatbot import generate_chat_response, FullRequest
from module_emotionReport import generate_messages_response, messagesRequest
import os
from typing import List

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from module_love import infer_ai


app = FastAPI()
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React 앱의 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# @app.post("/love")
# async def read_fastapi(text: str = Form()):
#     result = infer_ai(text)
#     return result

@app.post("/process")
async def process_file(request: Request):
    data = await request.json()
    print("data", data)
    user_id = data['user_id']
    content = data['content']

    # result = infer_ai(content)
    result = {
        "answer": "처리 결과",
        "analyze": content[:20]
    }
    print(f"\nresult:{result}")

    return result

#uvicorn main:app --reload --port=8001

