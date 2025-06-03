import os
from transformers import AutoTokenizer, AutoModelForCausalLM

class ModelManager:
    def __init__(self):
        self.model_dir = "model_cache"
    
    def load_model(self, model_name: str = "facebook/opt-125m") -> tuple[AutoModelForCausalLM, AutoTokenizer]:
        # Create model directory if it doesn't exist
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Load model and tokenizer
        model = AutoModelForCausalLM.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        return model, tokenizer