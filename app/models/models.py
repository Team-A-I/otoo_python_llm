from openai import OpenAI
import os
from fastapi import HTTPException
from db.db_util import get_model_name
from prompts.prompts import conflict_prompt, love_prompt, emotion_report_prompt, chatbot_prompt_mode_2, chatbot_prompt_default

api_key = os.getenv('OPENAI_API_KEY')

class EmotionReportModel:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.model_name = get_model_name()

    def generate_messages_response(self, text):
        messages = [
            {"role": "system", "content": emotion_report_prompt},
            {"role": "user", "content": text}
        ]

        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=1,
                max_tokens=1000,
                top_p=0.5,
                frequency_penalty=0,
                presence_penalty=0
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error calling OpenAI API: {str(e)}")

        return completion.choices[0].message.content.strip()

class ChatbotModel:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.model_name = get_model_name()

    def generate_chat_response(self, mode, recent_messages):
        if mode == '2':
            prompt = chatbot_prompt_mode_2
        else:
            prompt = chatbot_prompt_default

        messages = [{"role": "system", "content": prompt}]
        for message in recent_messages:
            role, content = message.split(" : ", 1)
            messages.append({"role": role, "content": content})

        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.6,
                max_tokens=256,
                top_p=0.5,
                frequency_penalty=0,
                presence_penalty=0
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error calling OpenAI API: {str(e)}")

        return completion.choices[0].message.content.strip()

class AnalysisModel:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.model_name = get_model_name()

    def analyze(self, text, analysis_type):
        if analysis_type == 'conflict':
            prompt = conflict_prompt
        elif analysis_type == 'love':
            prompt = love_prompt
        else:
            raise HTTPException(status_code=400, detail="Invalid analysis type")

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()

emotion_report_model = EmotionReportModel(api_key=api_key)
chatbot_model = ChatbotModel(api_key=api_key)
analysis_model = AnalysisModel(api_key=api_key)

def get_emotion_report_model():
    return emotion_report_model

def get_chatbot_model():
    return chatbot_model

def get_analysis_model():
    return analysis_model