from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from models.models import FriendshipModel, get_friendship_model
from modules.module_friendship import get_friendship_response

class TextMessage(BaseModel):
    text: str

router = APIRouter()

@router.post("/friendship")
def process_data(message: TextMessage, model: FriendshipModel = Depends(get_friendship_model)):
    try:
        response = get_friendship_response(message.text, model)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))