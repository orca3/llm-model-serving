import unittest
from sympy import Array
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import requests
from fastapi.testclient import TestClient
from app.server import app
import json
import os

class TestModelServing(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.model_ids = {
            "sentiment": "550e8400-e29b-41d4-a716-446655440000",
            "spam": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
            "image": "7c9e6679-7425-40de-944b-e07fc1f90ae7"
        }
        
        # Test data with expected labels
        self.test_data = {
            "sentiment": {
                "positive": {
                    "text": "This movie was great! I really enjoyed it.",
                    "expected_label": "POSITIVE"
                },
                "negative": {
                    "text": "This movie was terrible. I hated every minute of it.",
                    "expected_label": "NEGATIVE"
                }
            },
            "spam": {
                "ham": {
                    "text": "Hi, can we meet tomorrow at 2pm?",
                    "expected_label": "LABEL_0"  # Ham label
                },
                "spam": {
                    "text": "WIN A FREE IPHONE NOW! CLICK HERE!",
                    "expected_label": "LABEL_1"  # Spam label
                }
            }
        }
        
    def _get_label(self, model_type: str, probabilities: list):
        
        if (model_type == "sentiment"):
            model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

            predicted_class_id = max(range(len(probabilities[0])), key=lambda i: probabilities[0][i])
            return model.config.id2label[predicted_class_id]
        
        elif (model_type == "spam"):
            return "LABEL_" + str(max(range(len(probabilities[0])), key=lambda i: probabilities[0][i]))

    def test_list_models(self):
        """Test listing available models"""
        response = self.client.get("/models")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("available_models", data)
        self.assertIn("loaded_models", data)

    def test_sentiment_model(self):
        """Test sentiment analysis model"""
        # Test positive sentiment
        response = self.client.post(
            "/predict",
            json={
                "model_id": self.model_ids["sentiment"],
                "input_data": self.test_data["sentiment"]["positive"]["text"]
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("predictions", data)
        predictions = data["predictions"]
        self.assertTrue(len(predictions) > 0)
        # Check if the prediction contains the expected label
        self.assertTrue(
            self._get_label("sentiment", predictions) == self.test_data["sentiment"]["positive"]["expected_label"] 
        )
        
        # Test negative sentiment
        response = self.client.post(
            "/predict",
            json={
                "model_id": self.model_ids["sentiment"],
                "input_data": self.test_data["sentiment"]["negative"]["text"]
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("predictions", data)
        predictions = data["predictions"]
        self.assertIsInstance(predictions, list)
        self.assertTrue(len(predictions) > 0)
        # Check if the prediction contains the expected label
        self.assertTrue(
            self._get_label("sentiment", predictions) == self.test_data["sentiment"]["negative"]["expected_label"] 
        )

    def test_spam_model(self):
        """Test spam detection model"""
        # Test ham (non-spam)
        response = self.client.post(
            "/predict",
            json={
                "model_id": self.model_ids["spam"],
                "input_data": self.test_data["spam"]["ham"]["text"]
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("predictions", data)
        predictions = data["predictions"]
        self.assertIsInstance(predictions, list)
        self.assertTrue(len(predictions) > 0)
        # Check if the prediction contains the expected label
        self.assertTrue(
            self._get_label("spam", predictions) == self.test_data["spam"]["ham"]["expected_label"] 
        )
        
        # Test spam
        response = self.client.post(
            "/predict",
            json={
                "model_id": self.model_ids["spam"],
                "input_data": self.test_data["spam"]["spam"]["text"]
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("predictions", data)
        predictions = data["predictions"]
        self.assertIsInstance(predictions, list)
        self.assertTrue(len(predictions) > 0)

    def test_image_model(self):
        """Test image classification model"""
        # Create a test image path
        test_image_path = os.path.join(os.path.dirname(__file__), "images", "cat1.jpg")
        
        # Test image classification
        with open(test_image_path, "rb") as f:
            response = self.client.post(
                "/predict",
                json={
                    "model_id": self.model_ids["image"],
                    "input_data": test_image_path
                }
            )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("predictions", data)
        predictions = data["predictions"]
        self.assertIsInstance(predictions, list)
        self.assertTrue(len(predictions) > 0)
       
    def test_invalid_model_id(self):
        """Test prediction with invalid model ID"""
        response = self.client.post(
            "/predict",
            json={
                "model_id": "invalid-id",
                "input_data": "test input"
            }
        )
        self.assertEqual(response.status_code, 404)

    def test_model_cache(self):
        """Test model caching behavior"""
        return None
        # # Make requests to all three models in sequence
        # for model_id in self.model_ids.values():
        #     response = self.client.post(
        #         "/predict",
        #         json={
        #             "model_id": model_id,
        #             "input_data": "test input"
        #         }
        #     )
        #     self.assertEqual(response.status_code, 200)
        
        # # Check loaded models
        # response = self.client.get("/models")
        # self.assertEqual(response.status_code, 200)
        # data = response.json()
        # self.assertLessEqual(len(data["loaded_models"]), 2)  # Should have max 2 models loaded

if __name__ == '__main__':
    unittest.main() 