import os, torch
import matplotlib.pyplot as plt
import numpy as np
import timm
from main import prepare_dataloaders

MODEL_DIR = os.path.join("models", "current_model")
MODEL = "model.pt"
DATA_DIR = os.path.join("test_data")

def visualize_model(dataloaders, model, class_names, num_images=6, device="cpu"):
    """Validate model and visualize with N images"""
    was_training = model.training
    model.eval()
    images_so_far = 0
    print(num_images)
    plt.figure()

    # Transformations
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])

    with torch.no_grad():
        for i, (inputs, labels) in enumerate(dataloaders['valid']):
            inputs = inputs.to(device)
            labels = labels.to(device)

            # Forward pass
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            probs = torch.sigmoid(outputs)

            # Go through images and display
            for j in range(inputs.size()[0]):
                images_so_far += 1
                plt.subplot(num_images//2, 2, images_so_far)
                plt.axis('off')
                plt.title(f'predicted: {class_names[preds[j]]} {probs[j][preds[j]]:.3f}')
                # Prepare image
                inp = inputs.cpu().data[j]
                inp = inp.numpy().transpose((1, 2, 0))
                inp = std * inp + mean
                inp = np.clip(inp, 0, 1)
                plt.imshow(inp)
    plt.show()
    input("Press any key!")
    model.train(mode=was_training)

if __name__ == "__main__":
    # Device agnostic 
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Inits
    model_path = os.path.join(MODEL_DIR, MODEL)

    # Prepare data
    dataloaders, dataset_sizes, class_names = prepare_dataloaders(DATA_DIR)

    # Load model
    model = timm.create_model(
        "resnet10t",
        pretrained=True,
        num_classes = 2
    )
    model.to(device)
    model.load_state_dict(torch.load(model_path, weights_only=True))

    # Visualize
    visualize_model(dataloaders, model, class_names, dataset_sizes["valid"], device)