from app.store import ModelMetadata
from app.worker import ModelWorker

class ModelEngine:
    workers = {} # {model_id: worker}
    
    def __init__(self):
        self.workers = {} 
    
    def get_worker(self, model_metadata: ModelMetadata):
        if model_metadata.id not in self.workers:
            self.workers[model_metadata.id] = ModelWorker(model_metadata.id)
        return self.workers[model_metadata.id]
    
    def create_worker(self, model_metadata: ModelMetadata):
        if model_metadata.id not in self.workers:
            self.workers[model_metadata.id] = ModelWorker(model_metadata.id)
        return self.workers[model_metadata.id]
    
    def delete_worker(self, model_metadata: ModelMetadata):
        if model_metadata.id in self.workers:
            del self.workers[model_metadata.id]