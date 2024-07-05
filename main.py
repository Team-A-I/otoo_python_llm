
# main.py

from pydantic import BaseModel
import logging
from module_conflict import get_chatgpt_response

# 로그 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from openai import OpenAI
from dotenv import load_dotenv
from module_chatbot import generate_chat_response, FullRequest
from module_emotionReport import generate_messages_response, messagesRequest
import os
from typing import List
from fastapi import FastAPI, Request , HTTPException
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
    #print("data", data)
    user_id = data['user_id']
    content = data['content']

    result = infer_ai(content)
    # result = {
    #     "answer": "처리 결과",
    #     "analyze": content[:20]
    # }
    #print(f"\nresult:{result}")

    return result

#정현 -----------------------------------------------------------
class Message(BaseModel):
    id: int
    text: str

@app.post("/conflict")
async def process_data(messages: list[Message]):
    try:
        message_dicts = [message.dict() for message in messages]
        response = get_chatgpt_response(message_dicts)
        return {"response": response}
    except Exception as e:
        logger.error("Error processing data: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))

#uvicorn main:app --reload --port 8001

