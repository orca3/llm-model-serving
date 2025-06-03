from fastapi import FastAPI
from pydantic import BaseModel
from llm import LLM

app = FastAPI()
llm = LLM()

class GenerateRequest(BaseModel):
    prompt: str

class GenerateResponse(BaseModel):
    generated_text: str

@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    generated_text = llm.generate(request.prompt)
    return GenerateResponse(generated_text=generated_text)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 