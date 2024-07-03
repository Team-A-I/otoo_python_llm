import pandas as pd
import os
import time, random
from dotenv import load_dotenv
import re
import json
from openai import OpenAI

# 데이터 입력

## chat-GPT활용
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

##프롬프트 입력해서 GPT돌리기
def infer_ai(Text):
    delimiter = "####"

    format = """ 
    {
     "total_score":{
        "name,":num,
        "name":num
    },
    "support":{
        "name":{
            "score":num,
            "reason":str (short, a line)
        },
        "name":{
            "score":num,
            "reason":str (short, a line)
        }
    },
    "cheat":{
        "name":{
            "score":num,
            "reason":str (short, a line)
        },
        "name":{
            "score":num,
            "reason":str (short, a line)
        }
    },
    "sexual":{
        "name":{
            "score":num,
            "reason":str (short, a line)
        },
        "name":{
            "score":num,
            "reason":str (short, a line)
        }
    },
    "interest":{
        "name":{"a","b","c"},
        "name":{"a","b","c"}
    }
    }
    """

    Prompt = f"""
    ##Order
    You are an expert in analyzing conversations between romantic partners. You need to express the analysis results quantitatively and explain why those results were obtained. In a conversation between two people, answer who scores higher based on the given criteria, and the total score must be 100 points. Always find the judgment criteria from the {delimiter}text and explain it. Answer in Korean and make sure to base your findings solely on the provided text. Remember who said what and respond accordingly. Follow the Format below.
    Person A's affection score: X points, Person B's affection score: Y points (ensure the total is 100 points.) List each name in the text and use their name in the format.

    ##Contents
    1. Person A likes Person B more.
    2. Who is more considerate? (Ensure the total is 100 points).
    3. Who is more likely to cheat in the future? (Ensure the total is 100 points).
    4. Who is more sexually attracted to the other person? (Ensure the total is 100 points).
    5. What are each person's interests? (Extract 3 nouns each).

    ##Format json
    {format}
    """

    messages = [{'role': 'system', 'content': Prompt},
                {'role': 'user', 'content': f'{delimiter}{Text}.'}]

    print(f"\nmessages here:{messages}")

    chat = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
        messages=messages,
        response_format ={"type": "json_object"},
        temperature=0.6)

    reply = chat.choices[0].message.content
    reply = json.loads(reply)
    # print(f'ChatGPT: {reply}')

    try:
        result = reply
    except Exception as e:
        result = "Error"

    return result