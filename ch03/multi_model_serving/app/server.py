from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from typing import Any, Dict, Optional
import uvicorn
import os
from .store import ModelStore
from .manager import ModelManager

app = FastAPI(title="Multi-Model Serving Demo")

# Initialize components
model_store = ModelStore("config/models.json")
model_manager = ModelManager(model_store)

class PredictionRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    model_id: str
    input_data: Any

@app.post("/predict")
async def predict(request: PredictionRequest):
    # Get model worker
    worker = model_manager.get_model_worker(request.model_id)
    if not worker:
        raise HTTPException(status_code=404, detail=f"Model {request.model_id} not found")
    
    # Make prediction
    try:
        result = worker.predict(request.input_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
async def list_models():
    return {
        "available_models": model_store.list_models(),
        "loaded_models": model_manager.list_loaded_models()
    }

if __name__ == "__main__":
    # Get port from environment variable or use default 8001
    port = int(os.getenv("PORT", "8001"))
    uvicorn.run(app, host="0.0.0.0", port=port) 