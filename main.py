from fastapi import FastAPI

app = FastAPI()

@app.get("/llm-endpoint")
def read_fastapi():
    return {"message": "Hello from llm"}
