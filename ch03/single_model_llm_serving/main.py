from fastapi import FastAPI, BackgroundTasks, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from llm import LLM
from typing import List
import asyncio
import multiprocessing
import atexit
import signal

# Create FastAPI app
app = FastAPI()

# Create LLM instance
_llm = None
_llm_lock = multiprocessing.Lock()

def cleanup():
    global _llm
    if _llm is not None:
        try:
            _llm._cleanup()
        except:
            pass
        _llm = None

def get_llm():
    global _llm
    with _llm_lock:
        if _llm is None:
            _llm = LLM()
            # Register cleanup
            atexit.register(cleanup)
        return _llm

class GenerateRequest(BaseModel):
    prompt: str

class GenerateResponse(BaseModel):
    generated_text: str

class BatchGenerateRequest(BaseModel):
    prompts: List[str]

class BatchGenerateResponse(BaseModel):
    generated_texts: List[str]

@app.post("/generate_stream")
async def generate_stream(request: GenerateRequest, llm: LLM = Depends(get_llm)):
    async def event_generator():
        loop = asyncio.get_event_loop()
        async for token in llm.event_generator(loop, request.prompt):
            # token = 'data: {"token": " a", "sequence_id": "8310f5e1-6f6f-480e-b2f9-c8144a12cc17"}\n\n'
            yield token
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )

# process 1 request with only one prompt at a time.
@app.post("/basic_generate", response_model=GenerateResponse)
async def basic_generate(request: GenerateRequest, llm: LLM = Depends(get_llm)):
    generated_text = llm.basic_generate(request.prompt)
    return GenerateResponse(generated_text=generated_text)

# process multiple prompts in a request
@app.post("/generate", response_model=BatchGenerateResponse)
async def generate(request: BatchGenerateRequest, llm: LLM = Depends(get_llm)):
    generated_texts = llm.generate(request.prompts)
    return BatchGenerateResponse(generated_texts=generated_texts)

def signal_handler(signum, frame):
    cleanup()
    exit(0)

if __name__ == "__main__":
    import uvicorn
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Initialize LLM before starting the server
    get_llm()
    uvicorn.run(app, host="0.0.0.0", port=8000) 