from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from openai import OpenAI
import logging

# 환경 변수 로드
load_dotenv()

# 로그 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class Message(BaseModel):
    id: int
    text: str


@app.post("/process")
async def process_data(messages: list[Message]):
    format ="""
            {
            "wrong_percentage": {
                "name1": num,
                "name2": num
            },
            "conflict_cause_percentage": {
                "cause1": num,
                "cause2": num,
                "cause3": num,
                "cause4": num,
                "cause5": num,
            },

            "mbti_tendency_percentage": {
                "name1": num,
                "name2": num,
            },

            "offended_percentage": {
                "name1": num,
                "name2": num
            },
            "tactless_percentage": {
                "name1": num,
                "name2": num
            },
            "priority_keywords": {
                "name1": ["keywords1", "keywords2", "keywords3", "keywords4", "keywords5"],
                "name2": ["keywords1", "keywords2", "keywords3", "keywords4", "keywords5"]
            },
            "conflict_resolution_advice": {
                "very_lively_and_positive_personality": str,
                "very_hot_and_straightforward_personality": str,
                "very_timid_sad_and_hesitant_personality": str
            }
            }"""
    
    delimeter = "###"
    
    try:
        system_prompt = f"""
            "##Order
            You have to give me the answer I want from the given text. 1. Indicate in % who is at fault in this altercation. 
            2. In the conversation between the two, show the cause of the conflict in %.
            3. Indicate in % who is more MBTI 'T' sullen, who is more offended, and who is more tactless. 
               Additionally, provide a one-sentence explanation for each result.
            4. In the conversation, show the Top 5 with a simple word keyword what the priorities each think of.
            5. How to resolve the conflict between two people 
            5-1. The 'very lively and positive personality' character gives pleasant and funny advice. 
            5-2. The character in 'a very hot and straightforward personality' gives impulsive and clear advice, 
                 but speaks like a cursing grandfather.
            5-3. Very timid, sad and hesitant' character gives vague advice from a neutral standpoint. Please answer in Korean.
            Follow below format.
            
            ##Format
            {format}
            """
        user_input = "\n".join([message.text for message in messages])
        
        logger.info("User input: %s", user_input)
        
        # OpenAI API 호출
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content":  user_input}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        # 응답 메시지 접근 방식 수정
        logger.info("OpenAI API response: %s", response)
        message_content = response.choices[0].message.content.strip()
        return {"response": message_content}
    except Exception as e:
        logger.error("Error processing data: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('FASTAPI_PORT')))


      
# uvicorn main:app --reload --port 8001
