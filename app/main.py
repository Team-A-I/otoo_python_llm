from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from api.emotion_report_router import router as emotion_report_router
from api.chatbot_router import router as chatbot_router
from api.analysis_router import router as analysis_router

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

# 라우터 등록
app.include_router(emotion_report_router)
app.include_router(chatbot_router)
app.include_router(analysis_router)

# uvicorn main:app --reload --port 8001