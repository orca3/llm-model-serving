from collections import OrderedDict
from typing import Dict, Optional
from .store import ModelStore
from .worker import ModelWorker

class ModelManager:
    def __init__(self, model_store: ModelStore, max_models: int = 2):
        self.model_store = model_store
        self.max_models = max_models
        self.model_cache = OrderedDict()  # OrderedDict to track least recently used
    
    def get_model_worker(self, model_id: str) -> Optional[ModelWorker]:
        # Check if model is in cache
        if model_id in self.model_cache:
            # Move to end (most recently used)
            worker = self.model_cache.pop(model_id)
            self.model_cache[model_id] = worker
            return worker
        
        # Get model metadata
        model_metadata = self.model_store.get_model(model_id)
        if not model_metadata:
            return None
        
        # Check if we need to remove least used model
        if len(self.model_cache) >= self.max_models:
            # Remove least recently used model
            self.model_cache.popitem(last=False)
        
        # Create and cache new model worker
        worker = ModelWorker(model_metadata)
        self.model_cache[model_id] = worker
        return worker
    
    def list_loaded_models(self) -> Dict[str, str]:
        return {model_id: worker.model_metadata.name 
                for model_id, worker in self.model_cache.items()} 