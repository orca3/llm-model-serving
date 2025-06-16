import uuid
from typing import List, Dict, Any, Optional
from queue import Queue
import asyncio

class Sequence:
    def __init__(self, seq_id: str, prompt: str, client_stream, loop):
        self.id = seq_id
        self.prompt = prompt
        self.output = []
        self.finished = False
        self.loop = loop
        self.client_stream = client_stream
        self.token_count = 0

class WorkloadManager:
    def __init__(self):
        self.incoming_queue: Queue[Sequence] = Queue()
        self.active_sequences: List[Sequence] = []
        
        self.incoming_streaming_queue: Queue[Sequence] = Queue()
        self.active_streaming_sequences: List[Sequence] = []
        self.batch_size = 4  # Process up to 4 sequences at a time
        self.sequence_map: Dict[str, Sequence] = {}
    
    # for basic generate and batch generate        
    def add_request(self, prompt: str) -> str:
        request_id = str(uuid.uuid4())
        sequence = Sequence(request_id, prompt, None, None)
        self.incoming_queue.put(sequence)
        self.sequence_map[request_id] = sequence
        return request_id
    
    # for streaming generate
    def add_streaming_request(self, prompt: str, client_stream, loop) -> str:
        request_id = str(uuid.uuid4())
        sequence = Sequence(request_id, prompt, client_stream, loop)
        self.incoming_streaming_queue.put(sequence)
        self.sequence_map[request_id] = sequence
        return request_id
    
    def get_next_batch(self, is_streaming: bool = False) -> List[Sequence]:
        if is_streaming:
            while len(self.active_streaming_sequences) < self.batch_size and not self.incoming_streaming_queue.empty():
                sequence = self.incoming_streaming_queue.get()
                self.active_streaming_sequences.append(sequence)
        
            return self.active_streaming_sequences
        else:
            while len(self.active_sequences) < self.batch_size and not self.incoming_queue.empty():
                sequence = self.incoming_queue.get()
                self.active_sequences.append(sequence)
                
            return self.active_sequences
    
    def remove_active_sequence(self, seq_id: str):
        if seq_id in self.sequence_map:
            sequence = self.sequence_map[seq_id]
            if sequence in self.active_sequences:
                self.active_sequences.remove(sequence)
            if sequence in self.active_streaming_sequences:
                self.active_streaming_sequences.remove(sequence)
    
    def remove_finished_sequence(self, seq_id: str):
        if seq_id in self.sequence_map:
            sequence = self.sequence_map[seq_id]
            if sequence in self.active_sequences:
                self.active_sequences.remove(sequence)
            if sequence in self.active_streaming_sequences:
                self.active_streaming_sequences.remove(sequence)
            del self.sequence_map[seq_id]
            
    def is_sequence_finished(self, seq_id: str) -> bool:
        if seq_id in self.sequence_map:
            sequence = self.sequence_map[seq_id]
            return sequence.finished
        return False
    
    def get_sequence(self, seq_id: str) -> Optional[Sequence]:
        return self.sequence_map.get(seq_id)
    
    def update_sequence_output(self, seq_id: str, token: str, is_finished: bool = False):
        if seq_id in self.sequence_map:
            sequence = self.sequence_map[seq_id]
            sequence.output.append(token)
            sequence.prompt += token
            sequence.token_count += 1
            sequence.finished = is_finished
            return sequence
        return None 