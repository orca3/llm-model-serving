import unittest
import requests
import numpy as np
from PIL import Image
import tritonclient.http as httpclient
import tritonclient.utils as utils
import os

class TestTritonDenseNet(unittest.TestCase):
    def setUp(self):
        self.triton_url = "0.0.0.0:8009"
        self.model_name = "densenet_onnx"
        self.client = httpclient.InferenceServerClient(url=self.triton_url)
        
        # Test image path - you'll need to provide a test image
        self.test_image_path = os.path.join(os.path.dirname(__file__), "images", "cat1.jpg")
        
    def test_model_loading(self):
        """Test loading the model through Triton management API"""
        # Load model
        load_url = f"http://{self.triton_url}/v2/repository/models/{self.model_name}/load"
        response = requests.post(load_url)
        self.assertEqual(response.status_code, 200, "Failed to load model")
        
    def test_model_unloading(self):
        """Test unloading the model through Triton management API"""
        # Unload model
        unload_url = f"http://{self.triton_url}/v2/repository/models/{self.model_name}/unload"
        response = requests.post(unload_url)
        self.assertEqual(response.status_code, 200, "Failed to unload model")
        
    def test_model_inference(self):
        """Test making predictions with the loaded model"""
        # First load the model
        load_url = f"http://{self.triton_url}/v2/repository/models/{self.model_name}/load"
        requests.post(load_url)
        
        # Load and preprocess image
        img = Image.open(self.test_image_path)
        img = img.resize((224, 224))  # DenseNet expects 224x224 images
        img_array = np.array(img).astype(np.float32)
        
        # Normalize image
        img_array = img_array / 255.0
        img_array = np.transpose(img_array, (2, 0, 1))  # Change to CHW format
        # Remove batch dimension expansion since model expects [3,224,224]
        
        # Prepare input
        input_tensor = httpclient.InferInput("data_0", img_array.shape, "FP32")
        input_tensor.set_data_from_numpy(img_array)
        
        # Make inference request
        response = self.client.infer(
            model_name=self.model_name,
            inputs=[input_tensor],
            outputs=[httpclient.InferRequestedOutput("fc6_1")]
        )
        
        # Get predictions
        predictions = response.as_numpy("fc6_1")
        
        # Basic assertions
        self.assertIsNotNone(predictions, "No predictions received")
        self.assertEqual(predictions.shape, (1000,), "Expected shape (1000,) for ImageNet predictions")
        
        # Get top prediction
        top_prediction = np.argmax(predictions)
        self.assertIsInstance(top_prediction, np.integer, "Top prediction should be an integer")
        
        # Clean up - unload model
        unload_url = f"http://{self.triton_url}/v2/repository/models/{self.model_name}/unload"
        requests.post(unload_url)

if __name__ == '__main__':
    unittest.main() 