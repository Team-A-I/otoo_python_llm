from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from module_love import infer_ai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React 앱의 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.post("/love")
# async def read_fastapi(text: str = Form()):
#     result = infer_ai(text)
#     return result

@app.post("/process")
async def process_file(request: Request):
    data = await request.json()
    print("data", data)
    user_id = data['user_id']
    content = data['content']

    # result = infer_ai(content)
    result = {
        "answer": "처리 결과",
        "analyze": content[:20]
    }
    print(f"\nresult:{result}")

    return result

#uvicorn main:app --reload --port=8001