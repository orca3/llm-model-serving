import multiprocessing as mp
from typing import List, Dict, Any, Generator
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
        # Initialize state for streaming
        self.stream_states = {}  # request_id -> (input_ids, attention_mask, past_key_values)
    
    def generate(self, prompts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        logger.debug(f"Received prompts: {prompts}")
        results = []
        for prompt_data in prompts:
            inputs = self.tokenizer(prompt_data.prompt, return_tensors="pt").to(self.device)
            
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
                'request_id': prompt_data.id,
                'generated_text': generated_text
            })
        
        return results

    def generate_forward_batch(self, prompts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate one token for each prompt in the batch."""
        logger.debug(f"Received streaming prompts: {prompts}")
        
        # Add padding token to the tokenizer if not present
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Tokenize all prompts in batch
        encoded = self.tokenizer(
            [p['prompt'] for p in prompts],
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        ).to(self.device)
        
        logger.debug(f"Batch input shape: {encoded.input_ids.shape}")
        
        # Generate next token
        with torch.no_grad():
            outputs = self.model(
                input_ids=encoded.input_ids,
                attention_mask=encoded.attention_mask,
                use_cache=False
            )
            
            # Get next token logits and sample
            next_token_logits = outputs.logits[:, -1, :]
            next_token = torch.multinomial(
                torch.softmax(next_token_logits / 0.7, dim=-1),
                num_samples=1
            ).squeeze(-1)
            
            # Prepare results
            results = []
            for i, prompt_data in enumerate(prompts):
                token = self.tokenizer.decode(next_token[i].unsqueeze(0), skip_special_tokens=True)
                logger.debug(f"Generated token for prompt '{prompt_data['prompt']}': '{token}'")
                results.append({
                    'request_id': prompt_data['request_id'],
                    'token': token,
                    'is_finished': token == self.tokenizer.eos_token
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
            batch_data = task_queue.get()
            logger.debug(f"Received batch: {batch_data}")
            
            if batch_data is None:  # Shutdown signal
                logger.debug("Received shutdown signal")
                break
            
            batch, is_streaming = batch_data
            
            if is_streaming:
                # Handle streaming generation
                result_queue.put(('stream', worker.generate_forward_batch(batch)))
            else:
                # Handle regular generation
                result_queue.put(('complete', worker.generate(batch)))