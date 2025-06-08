from typing import Any, Dict, Optional
import torch
from abc import ABC, abstractmethod
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from torchvision.models import mobilenet_v2, MobileNet_V2_Weights
from PIL import Image
import torchvision.transforms as transforms

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