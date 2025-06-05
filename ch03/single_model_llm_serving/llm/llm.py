from typing import List, Dict, Any
from .workload_manager import WorkloadManager, Sequence
from .model_executor import ModelExecutor
import asyncio
import json
import atexit
import threading
import time
import uuid

class LLM:
    def __init__(self):
        self.model_executor = ModelExecutor()
        self.workload_manager = WorkloadManager()
        self.max_tokens = 20
        
        # Initialize the model
        self.model_executor.setup_worker("facebook/opt-125m")
        
        # Start processing loop in a separate thread
        self.thread = threading.Thread(target=self.requests_processing_loop, daemon=True)
        self.thread.start()
        
        # Register cleanup
        atexit.register(self._cleanup)
    
    def requests_processing_loop(self):
        """Process requests in a loop."""
        while True:
            try:
                active_sequences = self.workload_manager.get_next_batch(is_streaming=True)
                if not active_sequences:
                    time.sleep(0.1)
                    continue
                    
                # Process batch through model, forward pass.
                prompts = [{'prompt': seq.prompt, 'request_id': seq.id} for seq in active_sequences]
                prompts_results = self.model_executor.execute_forward_batch(prompts)
                
                # Stream tokens back to respective clients
                for result in prompts_results:
                    seq = self.workload_manager.get_sequence(result['request_id'])
                    if result['is_finished'] or seq.token_count > self.max_tokens:
                        # Use run_coroutine_threadsafe to safely put None in the main loop's queue
                        asyncio.run_coroutine_threadsafe(
                            seq.client_stream.put(None),
                            seq.loop
                        )
                        seq.finished = True
                        self.workload_manager.remove_finished_sequence(result['request_id'])
                    else:
                        # Use run_coroutine_threadsafe to safely put data in the main loop's queue
                        asyncio.run_coroutine_threadsafe(
                            seq.client_stream.put(
                                json.dumps({"token": result['token'], "sequence_id": result['request_id']})
                            ),
                            seq.loop
                        )
                        self.workload_manager.update_sequence_output(result['request_id'], result['token'])
                
            except Exception as e:
                print(f"Error in processing loop: {e}")
                time.sleep(0.1)
    
    def _cleanup(self):
        """Cleanup function to be called when the program exits."""
        # The thread will be automatically terminated since it's a daemon thread
        pass

    # process 1 request with only one prompt at a time.
    def basic_generate(self, prompt: str) -> str:

        sequence = Sequence(str(uuid.uuid4()), prompt, None, None)
        
        # Execute the batch
        results = self.model_executor.execute_batch([sequence])
        
        return results[1][0]['generated_text']

    # process multiple prompts in a request
    def generate(self, prompts: List[str]) -> List[str]:
        # Add all requests to workload manager
        request_ids = []
        for prompt in prompts:
            request_id = self.workload_manager.add_request(prompt)
            request_ids.append(request_id)
        
        # Process all requests in batches
        all_results = []
        while True:
            # Get next batch of requests
            sequences = self.workload_manager.get_next_batch()
            if not sequences:
                break
                
            # Execute the batch in one go
            results = self.model_executor.execute_batch(sequences)
            all_results.extend(results)
        
            # Map results back to original prompts
            generated_texts = []
            for request_id in request_ids:
                for result in all_results[1]:
                    if result['request_id'] == request_id:
                        generated_texts.append(result['generated_text'])
                        self.workload_manager.remove_finished_sequence(result['request_id'])
                        self.workload_manager.update_sequence_output(result['request_id'], result['generated_text'])
                        break
                else:
                    raise Exception(f"Result not found for request {request_id}")
        
        return generated_texts 
    
    async def event_generator(self, loop, prompt: str):
        
        asyncio.set_event_loop(loop)
        # Create a queue for this client's stream
        queue = asyncio.Queue()
        
        # Add streaming request to workload manager with the queue
        seq_id = self.workload_manager.add_streaming_request(prompt, queue, loop)
        
        print(f"Created queue for sequence {seq_id} in loop {id(loop)} and queue {id(queue._get_loop())}")  # Debug print
        
        try:
            while True:
                print(f"Waiting for data in queue for sequence {seq_id}")  # Debug print
                # Get next token from queue
                data = await queue.get()
                print(f"Received data in queue for sequence {seq_id}: {data}")  # Debug print
                if data is None:  # End of stream
                    print(f"End of stream for sequence {seq_id}")  # Debug print
                    break
                yield f"data: {data}\n\n"
        except Exception as e:
            print(f"Error in stream for sequence {seq_id}: {e}")
        finally:
            # Clean up
            self.workload_manager.remove_finished_sequence(seq_id)
            print(f"Cleaned up sequence {seq_id}")  # Debug print