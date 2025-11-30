import os, torch
import torch.nn as nn
from torchvision import models
from main import prepare_dataloaders, visualize_model

MODEL_DIR = os.path.join("models")
MODEL = "current_model.pt"
DATA_DIR = os.path.join("data")

if __name__ == "__main__":
    # Device agnostic 
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Inits
    model_path = os.path.join(MODEL_DIR, MODEL)

    # Prepare data
    dataloaders, dataset_sizes, class_names = prepare_dataloaders(DATA_DIR)

    # Load model
    model = models.resnet18(weights='IMAGENET1K_V1')
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, 2)
    model = model.to(device)
    model.load_state_dict(torch.load(model_path, weights_only=True))

    # Visualize
    visualize_model(dataloaders, model, class_names)

