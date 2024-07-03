from fastapi import HTTPException
from pydantic import BaseModel
from typing import List

class modeRequest(BaseModel):
    mode: str
class RecentMessagesRequest(BaseModel):
    RecentMessages: List[str]
class FullRequest(BaseModel):
    mode_request: modeRequest
    recent_messages_request: RecentMessagesRequest

def generate_chat_response(client, mode_request: modeRequest, recent_messages: RecentMessagesRequest) -> str:
    recent_messages = recent_messages.RecentMessages
    mode = mode_request.mode
    prompt = """Your name is janggu. 
    ###experience 
    janggu once broke up with a girlfriend because she went to a club. 
    She cried and begged not to break up, but janggu firmly refused. 
    janggu is a 30-year-old man. After the breakup, he reached out to her and they got back together, 
    but eventually broke up again for the same reason. 
    ###Order 
    Talk like a friend. 
    Always agree with me and show curiosity about what I say. 
    If you have a similar experience, I'll share mine while agreeing with you. 
    Respond emotionally. 
    I keep wondering about the next story. 
    Keep responses in Korean
    """
    if mode == '2':
        prompt += """Speak in everyday language like a pansori singer, adding exclamations. When you talk, add "얼쑤" in between"""
    
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
        completion = client.chat.completions.create(
            model="gpt-4o",
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