# Conflict_module.py
from module_pre import clean_chat

def get_chatgpt_response(client, messages):
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
    
    user_input = "\n".join([message["text"] for message in messages])
    # 데이터 전처리 적용하고 싶으면 하기!
    # clean_v = clean_chat(user_input)
    # print(f"clean_v : {clean_v}")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content":  user_input}
        ],
        max_tokens=3000,
        temperature=0.8
    )
    
    return response.choices[0].message.content.strip()
