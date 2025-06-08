from typing import Any, Dict
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from torchvision.models import mobilenet_v2, MobileNet_V2_Weights
from PIL import Image
import torchvision.transforms as transforms

class ModelWorker:
    def __init__(self, model_metadata):
        self.model_metadata = model_metadata
        self.model = None
        self.tokenizer = None
        self.transform = None
        self._load_model()
    
    def _load_model(self):
        if self.model_metadata.framework == "transformers":
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_metadata.name)
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_metadata.name)
        elif self.model_metadata.framework == "torchvision":
            self.model = mobilenet_v2(weights=MobileNet_V2_Weights.DEFAULT)
            self.model.eval()
            self.transform = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
    
    def predict(self, input_data: Any) -> Dict[str, Any]:
        if self.model_metadata.framework == "transformers":
            inputs = self.tokenizer(input_data, return_tensors="pt", padding=True, truncation=True)
            with torch.no_grad():
                outputs = self.model(**inputs)
            predictions = torch.softmax(outputs.logits, dim=-1)
            return {"predictions": predictions.tolist()}
        
        elif self.model_metadata.framework == "torchvision":
            if isinstance(input_data, str):
                image = Image.open(input_data).convert('RGB')
            else:
                image = input_data
            image_tensor = self.transform(image).unsqueeze(0)
            with torch.no_grad():
                outputs = self.model(image_tensor)
            predictions = torch.softmax(outputs, dim=1)
            return {"predictions": predictions.tolist()} 