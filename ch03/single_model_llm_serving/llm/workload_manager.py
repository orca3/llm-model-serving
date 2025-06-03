import uuid
from typing import List, Dict, Any

class WorkloadManager:
    def __init__(self):
        self.requests = []
        self.batch_size = 4  # Process up to 4 requests at a time
    
    def add_request(self, prompt: str) -> str:
        request_id = str(uuid.uuid4())
        self.requests.append({
            'request_id': request_id,
            'prompt': prompt
        })
        return request_id
    
    def get_next_batch(self) -> List[Dict[str, Any]]:
        if not self.requests:
            return []
        
        batch = self.requests[:self.batch_size]
        self.requests = self.requests[self.batch_size:]
        return batch 