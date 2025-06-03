from typing import List, Dict, Any
from .workload_manager import WorkloadManager
from .model_executor import ModelExecutor

class LLM:
    def __init__(self):
        self.model_executor = ModelExecutor()
        self.workload_manager = WorkloadManager()
        
        # Initialize the model
        self.model_executor.setup_worker("facebook/opt-125m")
    
    def generate(self, prompt: str) -> str:
        # Add request to workload manager
        request_id = self.workload_manager.add_request(prompt)
        
        # Get next batch of requests
        batch = self.workload_manager.get_next_batch()
        
        # Execute the batch
        results = self.model_executor.execute_batch(batch)
        
        # Find our result
        for result in results:
            if result['request_id'] == request_id:
                return result['generated_text']
        
        raise Exception("Result not found for request") 