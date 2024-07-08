# models.py
from openai import OpenAI
import os
import json
from fastapi import HTTPException
from db.db_util import get_model_name
from prompts.prompts import (emotion_report_prompt, chatbot_prompt_mode_2, 
                     chatbot_prompt_default, conflict_prompt, love_prompt,
                     friendship_prompt)

api_key = os.getenv('OPENAI_API_KEY')

class EmotionReportModel:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.model_name = get_model_name()

    async def generate_messages_response(self, messages_request):
        messages = messages_request.messages
        
        messages = [
            {
                "role": "system",
                "content": emotion_report_prompt
            },
            {
                "role": "user",
                "content": messages
            }
        ]
        
        try:
            completion = await self.client.chat.completions.create(
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

        content_value = completion.choices[0].message.content
        return content_value

class ChatbotModel:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.model_name = get_model_name()

    def generate_chat_response(self, mode_request, recent_messages_request):
        recent_messages = recent_messages_request.RecentMessages
        mode = mode_request.mode
        
        if mode == '2':
            prompt = chatbot_prompt_mode_2
        else:
            prompt = chatbot_prompt_default

        messages = [
            {
                "role": "system",
                "content": prompt
            }
        ]

        for message in recent_messages:
            role, content = message.split(" : ", 1)
            if role == 'user':
                messages.append({
                    "role": "user",
                    "content": content
                })
            elif role == 'assistant':
                messages.append({
                    "role": "assistant",
                    "content": content
                })

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
        content_value = completion.choices[0].message.content
        return content_value

class ConflictModel:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.model_name = get_model_name()

    def get_chatgpt_response(self, text):
        messages = [
                {"role": "system", "content": conflict_prompt},
                {"role": "user", "content":  text}
            ]
        
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0.8
        )
        
        return response.choices[0].message.content.strip()

class LoveModel:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.model_name = get_model_name()

    def infer_ai(self, text):
        delimiter = "####"

        messages = [{'role': 'system', 'content': love_prompt},
                    {'role': 'user', 'content': f'{delimiter}{text}.'}]

        try:
            chat = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                response_format={"type": "json_object"},
                temperature=0.6
            )

            reply = chat.choices[0].message.content
            reply = json.loads(reply)
            
            result = reply
        except Exception as e:
            result = "Error"

        return result

class FriendshipModel:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.model_name = get_model_name()

    def get_friendship_response(self, text):
        messages = [
                {"role": "system", "content": friendship_prompt},
                {"role": "user", "content":  text}
            ]
        
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0.8
        )
        
        return response.choices[0].message.content.strip()

emotion_report_model = EmotionReportModel(api_key=api_key)
chatbot_model = ChatbotModel(api_key=api_key)
conflict_model = ConflictModel(api_key=api_key)
love_model = LoveModel(api_key=api_key)
friendship_model = FriendshipModel(api_key=api_key)

def get_emotion_report_model():
    return emotion_report_model

def get_chatbot_model():
    return chatbot_model

def get_conflict_model():
    return conflict_model

def get_love_model():
    return love_model

def get_friendship_model():
    return friendship_model