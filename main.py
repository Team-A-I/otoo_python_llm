from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from models import emotion_report_model, chatbot_model, conflict_model, love_model, EmotionReportModel, ChatbotModel, ConflictModel, LoveModel
from module_emotionReport import messagesRequest, generate_messages_response
from module_chatbot import FullRequest, generate_chat_response
from module_conflict import get_chatgpt_response
from module_love import infer_ai
from pydantic import BaseModel
import logging

# 로그 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_emotion_report_model():
    return emotion_report_model

def get_chatbot_model():
    return chatbot_model

def get_conflict_model():
    return conflict_model

def get_love_model():
    return love_model

# 감정 보고서 생성 엔드포인트
@app.post("/emotionReport")
async def emotionReportLLM(messages_request: messagesRequest, model: EmotionReportModel = Depends(get_emotion_report_model)):
    response = generate_messages_response(model, messages_request)
    return response

# 챗봇 응답 생성 엔드포인트
@app.post("/chatbot")
async def chatbotLLM(full_request: FullRequest, model: ChatbotModel = Depends(get_chatbot_model)):
    mode_request = full_request.mode_request
    recent_messages_request = full_request.recent_messages_request
    response = generate_chat_response(model, mode_request, recent_messages_request)
    return response

# 연애 분석 엔드포인트
@app.post("/love")
async def process_file(request: Request, model: LoveModel = Depends(get_love_model)):
    try:
        data = await request.json()
        content = data['content']
        result = infer_ai(model, content)
        return result
    except Exception as e:
        logger.error("Error processing data: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))

# 갈등 분석 엔드포인트
class TextMessage(BaseModel):
    text: str

@app.post("/conflict")
async def process_data(message: TextMessage, model: ConflictModel = Depends(get_conflict_model)):
    try:
        response = get_chatgpt_response(message.text, model)
        return {"response": response}
    except Exception as e:
        logger.error("Error processing data: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))

# uvicorn main:app --reload --port 8001
