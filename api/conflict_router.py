# api/conflict_router.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from models.models import ConflictModel, get_conflict_model
from modules.module_conflict import get_chatgpt_response

class TextMessage(BaseModel):
    text: str

router = APIRouter()

@router.post("/conflict")
async def process_data(message: TextMessage, model: ConflictModel = Depends(get_conflict_model)):
    try:
        response = get_chatgpt_response(message.text, model)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
