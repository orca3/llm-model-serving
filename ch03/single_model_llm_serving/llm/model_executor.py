import multiprocessing as mp
from typing import List, Dict, Any
from .model_worker import ModelWorker
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

class ModelExecutor:
    def __init__(self):
        self.task_queue = mp.Queue()
        self.result_queue = mp.Queue()
        self.worker_process = None
        logger.debug("ModelExecutor initialized with queues")
    
    def setup_worker(self, model_name: str):
        logger.debug(f"Setting up worker with model: {model_name}")
        self.worker_process = mp.Process(
            target=ModelWorker.run,
            args=(model_name, self.task_queue, self.result_queue)
        )
        logger.debug("Starting worker process")
        self.worker_process.start()
        logger.debug("Worker process started")
    
    def execute_batch(self, prompts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not prompts:
            logger.debug("Empty batch received")
            return []
        
        logger.debug(f"Sending batch to worker: {prompts}")
        # Send batch to worker
        self.task_queue.put((prompts, False))
        
        # Get results
        logger.debug("Waiting for results from worker")
        results = self.result_queue.get()
        logger.debug(f"Received results from worker: {results}")
        return results
    
    def execute_forward_batch(self, prompts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not prompts:
            logger.debug("Empty batch received")
            return []
        
        logger.debug(f"Sending streaming batch to worker: {prompts}")
        # Send batch to worker with streaming flag
        self.task_queue.put((prompts, True))
        
        # Get streaming results
        logger.debug("Waiting for streaming results from worker")
        result_type, results = self.result_queue.get()
        logger.debug(f"Received streaming results from worker: {results}")
        
        if result_type == 'stream':
            return results
        else:
            raise Exception("Unexpected result type from worker")
    
    def __del__(self):
        if self.worker_process:
            logger.debug("Terminating worker process")
            self.worker_process.terminate()
            self.worker_process.join()
            logger.debug("Worker process terminated") 