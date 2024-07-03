from fastapi import HTTPException
from pydantic import BaseModel

class messagesRequest(BaseModel):
    messages: str

def generate_messages_response(client, messages_request: messagesRequest) -> str:
    messages = messages_request.messages

    prompt = """Read the user's conversation and create a message that expresses the user's feelings. 
                1. The format should be like a KakaoTalk message
                2. the recipient is the person who made the user feel hurt. 
                3. The sender of the kakaotalk message is the user. 
                4. Respond in Korean. 
                5. Just show the KakaoTalk message as the result only
                """
    
    messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": messages
                }
            ]
        }
    ]
    
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
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