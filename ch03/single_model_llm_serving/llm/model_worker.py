import multiprocessing as mp
from typing import List, Dict, Any
from .model_manager import ModelManager
import torch
import logging
import sys

# Set up logging with stream handler
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class ModelWorker:
    def __init__(self, model_name: str):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.debug(f"Loading model {model_name} on device {self.device}")
        self.model, self.tokenizer = ModelManager().load_model(model_name)
    
    def generate(self, prompts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        logger.debug(f"Received prompts: {prompts}")
        results = []
        for prompt_data in prompts:
            inputs = self.tokenizer(prompt_data['prompt'], return_tensors="pt").to(self.device)
            
            # Generate text
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs.input_ids,
                    max_length=50,
                    num_return_sequences=1,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            logger.debug(f"Generated text: {generated_text}")
            
            results.append({
                'request_id': prompt_data['request_id'],
                'generated_text': generated_text
            })
        
        return results
    
    @staticmethod
    def run(model_name: str, task_queue: mp.Queue, result_queue: mp.Queue):
        # Enable remote debugging
        logger.debug("Waiting for debugger to attach...")
        logger.debug("Debugger attached!")
        
        worker = ModelWorker(model_name)
        logger.debug("Worker initialized")
        
        while True:
            logger.debug("Waiting for batch from queue...")
            batch = task_queue.get()
            logger.debug(f"Received batch: {batch}")
            
            if batch is None:  # Shutdown signal
                logger.debug("Received shutdown signal")
                break
            
            results = worker.generate(batch)
            logger.debug(f"Sending results: {results}")
            result_queue.put(results) 