from fastapi import FastAPI, Request
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

@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI"}

# 라우터 등록
app.include_router(emotion_report_router)
app.include_router(chatbot_router)
app.include_router(analysis_router)

# 모든 예외 로깅
@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        raise

# uvicorn main:app --reload --port 8001
