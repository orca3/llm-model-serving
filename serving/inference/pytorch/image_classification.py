import io, json, re

import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image

class DenseNet:
    """
    Code is developed based on the following pytorch example: https://pytorch.org/tutorials/intermediate/flask_rest_api_tutorial.html
    """
    _instance = None

    @classmethod
    def load_densenet121_state_dict(cls):
        
        # '.'s are no longer allowed in module names, but previous _DenseLayer
        # has keys 'norm.1', 'relu.1', 'conv.1', 'norm.2', 'relu.2', 'conv.2'.
        # They are also in the checkpoints in model_urls. This pattern is used
        # to find such keys.
        pattern = re.compile(
            r"^(.*denselayer\d+\.(?:norm|relu|conv))\.((?:[12])\.(?:weight|bias|running_mean|running_var))$"
        )

        state_dict = torch.load(f='../models/densenet121/densenet121-a639ec97.pth', weights_only=True)
        for key in list(state_dict.keys()):
            res = pattern.match(key)
            if res:
                new_key = res.group(1) + res.group(2)
                state_dict[new_key] = state_dict[key]
                del state_dict[key]
    
        return state_dict

    def __new__(cls):
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(DenseNet, cls).__new__(cls)
            
            # intialize the model
            # Option (1), load model from internet. 
            # Make sure to set `weights` as `'IMAGENET1K_V1'` to use the pretrained weights:
            # cls._instance.model = models.densenet121(weights='IMAGENET1K_V1')

            # Option (2), load model from local. 
            # First, initialize model architecture
            cls._instance.model =  models.DenseNet(
                growth_rate = 32,
                block_config = (6, 12, 24, 16),
                num_init_features = 64,
                bn_size = 4,
                drop_rate = 0,
                num_classes = len(models.DenseNet121_Weights.IMAGENET1K_V1.meta["categories"]),
                memory_efficient = True)
            # Second, load model weights
            cls._instance.model.load_state_dict(cls.load_densenet121_state_dict())
            
            # Since we are using our model only for inference, switch to `eval` mode:
            cls._instance.model.eval()
            cls._instance.imagenet_class_index = json.load(open('../models/densenet121/imagenet_class_index.json'))
            
        return cls._instance

def transform_image(image_bytes):
    """
    Testing code for this function
    with open("../_static/img/sample_file.jpeg", 'rb') as f:
        image_bytes = f.read()
        tensor = transform_image(image_bytes=image_bytes)
        print(tensor)
    """
    my_transforms = transforms.Compose([transforms.Resize(255),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(image_bytes))
    
    return my_transforms(image).unsqueeze(0)

def get_prediction(image_bytes):
    """
    Testing code
    with open("../_static/img/sample_file.jpeg", 'rb') as f:
        image_bytes = f.read()
        print(get_prediction(image_bytes=image_bytes))
    """
    
    denseNet = DenseNet()
    tensor = transform_image(image_bytes=image_bytes)
    outputs = denseNet.model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    
    return denseNet.imagenet_class_index[predicted_idx]