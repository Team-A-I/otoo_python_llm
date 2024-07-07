import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_chatgpt_response(text):
    format = """
            {
            "wrong_percentage": {
                "name1": num,
                "name2": num
            },
            "conflict_cause_percentage": {
                "cause1": num, (korean)
                "cause2": num, (korean)
                "cause3": num, (korean)
                "cause4": num, (korean)
                "cause5": num, (korean)
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
                "name1": ["keywords1", "keywords2", "keywords3", "keywords4", "keywords5"], (korean)
                "name2": ["keywords1", "keywords2", "keywords3", "keywords4", "keywords5"] (korean)
            },
            "conflict_resolution_advice": {
                "positive_personality": str,
                "straightforward_personality": str,
                "timid_personality": str
            }
            }"""
    
    system_prompt = f"""
                    "##Order
                    You have to give me the answer I want from the given text. 1. Indicate in % who is at fault in this altercation. 
                    2. In the conversation between the two, show the cause of the conflict in %.
                    3. Indicate in % who is more MBTI 'T' sullen, who is more offended, and who is more tactless. 
                    Additionally, provide a one-sentence explanation for each result.
                    4. In the conversation, show the Top 5 with a simple word keyword what the priorities each think of.
                    5. How to resolve the conflict between two people:
                    5-1. The 'very lively and positive personality' character gives pleasant and funny advice. Please answer in detail and make the advice longer.
                    5-2. The character in 'a very hot and straightforward personality' gives impulsive and clear advice, but speaks like a cursing grandfather. Please elaborate and make the advice longer.
                    5-3. The 'very timid, sad and hesitant' character gives vague advice from a neutral standpoint. Please provide a longer and more detailed explanation. Must answer in Korean.

                    
                    ##Format
                    {format}
                    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content":  text}
        ],
        max_tokens=3000,
        temperature=0.8
    )
    
    return response.choices[0].message.content.strip()
