from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from api.emotion_report_router import router as emotion_report_router
from api.chatbot_router import router as chatbot_router
from api.analysis_router import router as analysis_router
from api.ocr_router import router as ocr_router
from dotenv import load_dotenv

load_dotenv()
# 로그 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_env_variables():
    print("DB_HOST:", os.getenv('DB_HOST'))
    print("DB_NAME:", os.getenv('DB_NAME'))
    print("DB_USER:", os.getenv('DB_USER'))
    print("DB_PASSWORD:", os.getenv('DB_PASSWORD'))

check_env_variables()

app = FastAPI()

origins = [
    "https://fastapi.otoo.kr",
    "https://react.otoo.kr",
    "https://restapi.otoo.kr",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#
@app.get("/health")
async def health_check():
    return {"message": "Welcome to FastAPI"}

# 라우터 등록
app.include_router(emotion_report_router)
app.include_router(chatbot_router)
app.include_router(analysis_router)
app.include_router(ocr_router)

# 모든 예외 로깅
@app.middleware("https")
async def log_exceptions(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        raise

# uvicorn main:app --reload --port 8001
