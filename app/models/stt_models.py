from pydantic import BaseModel
from typing import List, Dict
from prompts.prompts import single_speaker_prompt, multi_speaker_prompt
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
from fastapi import HTTPException
from db.db_util import get_model_name

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

class Utterance(BaseModel):
    start_at: int
    duration: int
    spk: int
    spk_type: str
    msg: str

class STTResponse(BaseModel):
    id: str
    status: str
    results: Dict[str, List[Utterance]]

class STTModel:
    def __init__(self, api_key):
        self.client = AsyncOpenAI(api_key=api_key)

    async def initialize(self):
        self.model_name = await get_model_name()

    async def analyze_stt(self, response: STTResponse):
        await self.initialize()
        speakers = {utterance.spk for utterance in response.results['utterances']}
        
        if len(speakers) == 1:
            conversation = ""
            for utterance in response.results['utterances']:
                conversation += f"I: {utterance.msg}\n"
            
            prompt = single_speaker_prompt.format(conversation=conversation)
        else:
            conversation = ""
            for utterance in response.results['utterances']:
                if utterance.spk == 0:
                    conversation += f"A: {utterance.msg}\n"
                else:
                    conversation += f"B: {utterance.msg}\n"
            
            prompt = multi_speaker_prompt.format(conversation=conversation)
        
        messages = [
            {"role": "system", "content": prompt}
        ]
        
        for utterance in response.results['utterances']:
            if len(speakers) == 1:
                messages.append({"role": "user", "content": f"I: {utterance.msg}"})
            else:
                if utterance.spk == 0:
                    messages.append({"role": "user", "content": f"A: {utterance.msg}"})
                else:
                    messages.append({"role": "user", "content": f"B: {utterance.msg}"})
        
        try:
            completion = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.7,
                max_tokens=3000
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error calling OpenAI API: {str(e)}")

        return completion.choices[0].message.content.strip()

stt_model = STTModel(api_key=api_key)

def get_stt_model():
    return stt_model
