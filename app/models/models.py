from openai import OpenAI
import os
from fastapi import HTTPException
from db.db_util import get_model_name
from prompts.prompts import conflict_prompt, love_prompt, friendship_prompt, emotion_report_prompt, chatbot_prompt_mode_2, chatbot_prompt_default
from modules.module_pre import clean_chat
from openai import AsyncOpenAI
from dotenv import load_dotenv
import base64
import requests
import json

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

class EmotionReportModel:
    def __init__(self, api_key):
        self.client = AsyncOpenAI(api_key=api_key)

    async def initialize(self):
        self.model_name = await get_model_name()

    async def generate_messages_response(self, messages_request):
        await self.initialize()
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
        self.client = AsyncOpenAI(api_key=api_key)

    async def initialize(self):
        self.model_name = await get_model_name()

    async def generate_chat_response(self, mode_request, recent_messages_request):
        await self.initialize()
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
            completion = await self.client.chat.completions.create(
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
    
class AnalysisModel:
    def __init__(self, api_key):
        self.client = AsyncOpenAI(api_key=api_key)

    async def initialize(self):
        self.model_name = await get_model_name()

    async def analyze(self, text, analysis_type):
        await self.initialize()
        if analysis_type == 'conflict':
            prompt = conflict_prompt
        elif analysis_type == 'love':
            prompt = love_prompt
        elif analysis_type == 'friendship':
            prompt = friendship_prompt
        else:
            raise HTTPException(status_code=400, detail="Invalid analysis type")

        try:
            text = clean_chat(text)
        except:
            text = text
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]

        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
class OcrModel:
    def __init__(self, api_key):
        self.model_name = get_model_name()
        self.ocrprompt = f'''The image above is a KakaoTalk conversation. White bubbles on the left are from the other person with a name, and yellow bubbles on the right are from the user. As an OCR expert, extract who said what in order. Name the yellow bubbles "User".'''

    async def ocrvision(self, image: bytes, analysis_type: str):
        if analysis_type == 'conflict':
            prompt = self.ocrprompt + '\n' + conflict_prompt
        elif analysis_type == 'love':
            prompt = self.ocrprompt + '\n' + love_prompt
        elif analysis_type == 'friendship':
            prompt = self.ocrprompt + '\n' + friendship_prompt
        else:
            raise HTTPException(status_code=400, detail="Invalid analysis type")

        base64_image = base64.b64encode(image).decode('utf-8')

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        result = response.json()
        # print("result",result)
        if 'choices' in result and len(result['choices']) > 0:
            content = result['choices'][0]['message']['content']
            content = content.strip('```json\n').strip('```')
            content = content.replace(",\n    }", "\n    }").replace(",\n    }", "\n    }")
            parsed_content = json.loads(content)
        else:
            print("No choices found in the response")

        return json.dumps(parsed_content, indent=2, ensure_ascii=False)

emotion_report_model = EmotionReportModel(api_key=api_key)
chatbot_model = ChatbotModel(api_key=api_key)
analysis_model = AnalysisModel(api_key=api_key)
ocr_model = OcrModel(api_key=api_key)

def get_emotion_report_model():
    return emotion_report_model

def get_chatbot_model():
    return chatbot_model

def get_analysis_model():
    return analysis_model

def get_ocr_model():
    return ocr_model