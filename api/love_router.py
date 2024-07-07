# api/love_router.py

from fastapi import APIRouter, Depends, HTTPException, Request
from models.models import LoveModel, get_love_model
from modules.module_love import infer_ai

router = APIRouter()

@router.post("/love")
async def process_file(request: Request, model: LoveModel = Depends(get_love_model)):
    try:
        data = await request.json()
        content = data['content']
        result = infer_ai(model, content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
