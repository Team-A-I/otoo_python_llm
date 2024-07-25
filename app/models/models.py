from openai import AsyncOpenAI
import os
from fastapi import HTTPException
from db.db_util import get_model_name
from prompts.prompts import conflict_prompt, love_prompt, friendship_prompt, emotion_report_prompt, chatbot_prompt_mode_2, chatbot_prompt_default, qna_prompt
from modules.module_pre import clean_chat
from dotenv import load_dotenv
from models.image_processor import ImageProcessor
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

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
        
        try:
            embeddings = OpenAIEmbeddings()
            loaded_vectorstore = FAISS.load_local("faiss/emotion_index", embeddings, allow_dangerous_deserialization=True)
            retriever = loaded_vectorstore.as_retriever()
            llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
            prompt = PromptTemplate.from_template(emotion_report_prompt)
            # 체인 설정
            chain = (
                {"context": retriever, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
            )
            question = messages
            response = chain.invoke(question)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error calling OpenAI API: {str(e)}")

        return response

class QnaModel:
    def __init__(self, api_key):
        self.client = AsyncOpenAI(api_key=api_key)

    async def initialize(self):
        self.model_name = await get_model_name()

    async def generate_qna_response(self, messages_request):
        await self.initialize()
        messages = messages_request.messages
        
        try:
            embeddings = OpenAIEmbeddings()
            loaded_vectorstore = FAISS.load_local("faiss/qna_index", embeddings, allow_dangerous_deserialization=True)
            retriever = loaded_vectorstore.as_retriever()
            llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
            prompt = PromptTemplate.from_template(qna_prompt)
            # 체인 설정
            chain = (
                {"context": retriever, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
            )
            question = messages
            response = chain.invoke(question)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error calling OpenAI API: {str(e)}")

        return response

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
        except Exception as e:
            f"지원하지 않는 데이터 형식: {str(e)}"

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
        self.client = AsyncOpenAI(api_key=api_key)
        self.image_processor = ImageProcessor()

    async def initialize(self):
        self.model_name = await get_model_name()

    async def analyze(self, text_data, analysis_type):
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
            text = f"상대방: {', '.join(text_data['상대방'])}\n나: {', '.join(text_data['나'])}"
        except:
            raise HTTPException(status_code=400, detail="Invalid analysis data")

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
    
    async def process_uploaded_files(self, files, type):
        results = await self.image_processor.process_images(files)
        all_left_text, all_right_text = results

        if not all_left_text and not all_right_text:
            raise ValueError("조건에 맞는 데이터를 넣어주세요")
        
        text_data = {
            "상대방": all_left_text,
            "나": all_right_text
        }
        
        analysis_result = await self.analyze(text_data, type)
        return analysis_result
    

emotion_report_model = EmotionReportModel(api_key=api_key)
chatbot_model = ChatbotModel(api_key=api_key)
analysis_model = AnalysisModel(api_key=api_key)
ocr_model = OcrModel(api_key=api_key)
qna_model = QnaModel(api_key=api_key)

def get_emotion_report_model():
    return emotion_report_model

def get_chatbot_model():
    return chatbot_model

def get_analysis_model():
    return analysis_model

ocr_model_instance = None

def get_ocr_model():
    global ocr_model_instance
    if ocr_model_instance is None:
        ocr_model_instance = ocr_model
    return ocr_model_instance

def get_qna_model():
    return qna_model
    

