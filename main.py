# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from conflict_module import get_chatgpt_response

# 로그 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

#uvicorn main:app --reload --port 8001