from collections import OrderedDict
from typing import Dict, Optional
from .store import ModelStore
from .worker import ModelWorker
from .engine import ModelEngine

class ModelManager:
    def __init__(self, model_store: ModelStore, max_models: int = 2):
        self.model_store = model_store
        self.max_models = max_models
        self.model_cache = OrderedDict()  # OrderedDict to track least recently used, id -> worker
        self.model_engine = ModelEngine()
    
    def get_model_worker(self, model_id: str) -> Optional[ModelWorker]:
        # Check if model is in cache
        if model_id in self.model_cache:
            # Move to end (most recently used)
            self.model_cache.move_to_end(model_id)
            return self.model_engine.get_worker(model_id)
        
        # Get model metadata
        model_metadata = self.model_store.get_model(model_id)
        if not model_metadata:
            return None
        
        # Check if we need to remove least used model
        if len(self.model_cache) >= self.max_models:
            # Remove least recently used model
            id, model_worker = self.model_cache.popitem(last=False)
            self.model_engine.delete_worker(id)
            
        # Download model if not already downloaded
        # Skip the downlaod implementation for simplicity
        # if not self.model_store.model_exists(model_id):
        #     self.model_store.download_model(model_id)
        
        # Create and cache new model worker
        self.model_cache[model_id] = self.model_engine.create_worker(model_metadata)
        return self.model_cache[model_id]
    
    def list_loaded_models(self) -> Dict[str, str]:
        return {model_id: worker.model_metadata.name 
                for model_id, worker in self.model_cache.items()} 