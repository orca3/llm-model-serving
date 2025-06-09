from typing import Any, Dict, Optional
import torch
from abc import ABC, abstractmethod
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from torchvision.models import mobilenet_v2, MobileNet_V2_Weights
from PIL import Image
import torchvision.transforms as transforms
import tritonclient.http as httpclient
import numpy as np
import requests
import os

class ModelWorker(ABC):
    def __init__(self, model_metadata):
        self.model_metadata = model_metadata
        self.model: Optional[torch.nn.Module] = None
        self._load_model()
    
    @abstractmethod
    def _load_model(self):
        pass
    
    @abstractmethod
    def predict(self, input_data: Any) -> Dict[str, Any]:
        pass

class TransformerWorker(ModelWorker):
    def __init__(self, model_metadata):
        self.tokenizer: Optional[AutoTokenizer] = None
        super().__init__(model_metadata)
    
    def _load_model(self):
        if self.model is None:  # Only load if not already loaded
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_metadata.name)
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_metadata.name)
    
    def predict(self, input_data: Any) -> Dict[str, Any]:
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Model or tokenizer not initialized")
        inputs = self.tokenizer(input_data, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        predictions = torch.softmax(outputs.logits, dim=-1)
        return {"predictions": predictions.tolist()}

class TorchVisionWorker(ModelWorker):
    def __init__(self, model_metadata):
        self.transform: Optional[transforms.Compose] = None
        super().__init__(model_metadata)
    
    def _load_model(self):
        if self.model is None:  # Only load if not already loaded
            self.model = mobilenet_v2(weights=MobileNet_V2_Weights.DEFAULT)
            self.model.eval()
            self.transform = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
    
    def predict(self, input_data: Any) -> Dict[str, Any]:
        if self.model is None or self.transform is None:
            raise RuntimeError("Model or transform not initialized")
        if isinstance(input_data, str):
            image = Image.open(input_data).convert('RGB')
        else:
            image = input_data
        image_tensor = self.transform(image).unsqueeze(0)
        with torch.no_grad():
            outputs = self.model(image_tensor)
        predictions = torch.softmax(outputs, dim=1)
        return {"predictions": predictions.tolist()}

class TritonWorker(ModelWorker):
    def __init__(self, model_metadata):
        self.triton_url = "0.0.0.0:8009"  # Default Triton server URL
        self.client = httpclient.InferenceServerClient(url=self.triton_url)
        super().__init__(model_metadata)
    
    def _load_model(self):
        """Load model through Triton management API"""
        load_url = f"http://{self.triton_url}/v2/repository/models/{self.model_metadata.name}/load"
        response = requests.post(load_url)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to load model: {response.text}")
        
        # Verify model is ready
        if not self.client.is_model_ready(self.model_metadata.name):
            raise RuntimeError("Model is not ready after loading")
    
    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make prediction through Triton inference API
        
        Args:
            input_data: Dictionary containing input tensors for the model
                Each key should be an input name and value should be a numpy array
                Example: {"data_0": np.array(...)}
        
        Returns:
            Dictionary containing output tensors from the model
                Each key is an output name and value is a numpy array
        """
        # Create input tensors
        inputs = []
        for name, data in input_data.items():
            if not isinstance(data, np.ndarray):
                # Convert list or other array-like data to numpy array
                try:
                    shape = data["shape"]
                    content = data["data"]
                    array = np.array(content, dtype=np.float32).reshape(shape)  # Explicitly set dtype to float32
                except:
                    raise ValueError(f"Input {name} could not be converted to a numpy array")
            else:
                array = data.astype(np.float32)  # Ensure existing numpy array is float32
            
            input_tensor = httpclient.InferInput(name, array.shape, "FP32")
            input_tensor.set_data_from_numpy(array)
            inputs.append(input_tensor)
        
        # Hardcode output name for DenseNet model
        output_name = "fc6_1"
        
        # Make inference request
        response = self.client.infer(
            model_name=self.model_metadata.name,
            inputs=inputs,
            outputs=[httpclient.InferRequestedOutput(output_name)]
        )
        
        # Get predictions and convert numpy arrays to lists for JSON serialization
        predictions = {
            output_name: response.as_numpy(output_name).tolist()
        }
        
        return predictions
    
    def __del__(self):
        """Cleanup: unload model when worker is destroyed"""
        try:
            unload_url = f"http://{self.triton_url}/v2/repository/models/{self.model_metadata.name}/unload"
            requests.post(unload_url)
        except:
            pass  # Ignore cleanup errors 