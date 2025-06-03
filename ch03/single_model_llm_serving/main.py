from fastapi import FastAPI
from pydantic import BaseModel
from llm import LLM
from typing import List

app = FastAPI()
llm = LLM()

class GenerateRequest(BaseModel):
    prompt: str

class GenerateResponse(BaseModel):
    generated_text: str

class BatchGenerateRequest(BaseModel):
    prompts: List[str]

class BatchGenerateResponse(BaseModel):
    generated_texts: List[str]

@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    generated_text = llm.generate(request.prompt)
    return GenerateResponse(generated_text=generated_text)

@app.post("/generate_batch", response_model=BatchGenerateResponse)
async def generate_batch(request: BatchGenerateRequest):
    generated_texts = llm.generate_batch(request.prompts)
    return BatchGenerateResponse(generated_texts=generated_texts)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 