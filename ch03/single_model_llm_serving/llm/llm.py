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

    def generate_batch(self, prompts: List[str]) -> List[str]:
        # Add all requests to workload manager
        request_ids = []
        for prompt in prompts:
            request_id = self.workload_manager.add_request(prompt)
            request_ids.append(request_id)
        
        # Process all requests in batches
        all_results = []
        while True:
            # Get next batch of requests
            batch = self.workload_manager.get_next_batch()
            if not batch:
                break
                
            # Execute the batch
            results = self.model_executor.execute_batch(batch)
            all_results.extend(results)
        
        # Map results back to original prompts
        generated_texts = []
        for request_id in request_ids:
            for result in all_results:
                if result['request_id'] == request_id:
                    generated_texts.append(result['generated_text'])
                    break
            else:
                raise Exception(f"Result not found for request {request_id}")
        
        return generated_texts 