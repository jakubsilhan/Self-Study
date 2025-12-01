import torch, json
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import torch.backends.cudnn as cudnn
import numpy as np
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import time
import os
from tempfile import TemporaryDirectory
import timm

MODEL_DIR = os.path.join("models")
MODEL_NAME = "current_model"
DATA_DIR = os.path.join("data")
LEARNING_RATE = 0.001
EPOCHS = 20

cudnn.benchmark = True
plt.ion()   # interactive mode

# Data augmentation and normalization for training

def prepare_dataloaders(data_dir):
    """Prepare dataloaders for training and validation"""
    # Data augmentation and normalization according to resnet
    data_transforms = {
        'train': transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'valid': transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }

    # Prepare data
    image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x), transform=data_transforms[x])
                    for x in ['train', 'valid']}
    dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=32,
                                                shuffle=True, num_workers=4)
                for x in ['train', 'valid']}
    dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'valid']}
    class_names = image_datasets['train'].classes

    return dataloaders, dataset_sizes, class_names


def train_model(dataloaders, model, criterion, optimizer, scheduler, dataset_sizes, num_epochs=25):
    """Train model and save best weights & stats safely."""
    # Inits
    since = time.time()
    final_model_path = os.path.join(MODEL_DIR, MODEL_NAME)
    os.makedirs(final_model_path, exist_ok=True)
    best_model_path = os.path.join(final_model_path, "best_model_ckp.pt")

    # Initialize tracking variables
    best_acc = 0.0
    train_losses, val_losses = [], []
    train_accs, val_accs = [], []

    try:
        for epoch in range(num_epochs):
            print(f'Epoch {epoch}/{num_epochs - 1}')
            print('-' * 10)

            # Training 
            model.train()
            running_loss = 0.0
            running_corrects = 0

            for inputs, labels in dataloaders["train"]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                # Zero grad
                optimizer.zero_grad()

                # Forward pass
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)

                # Loss
                loss = criterion(outputs, labels)

                # Backpropagation
                loss.backward()
                optimizer.step()

                # Per batch statistics
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels).item()

            # Per epoch statistics
            train_loss = running_loss / dataset_sizes["train"]
            train_acc = running_corrects / dataset_sizes["train"]
            print(f"Train Loss: {train_loss:.4f} Acc: {train_acc:.4f}")
            train_losses.append(train_loss)
            train_accs.append(train_acc)

            # Validation
            model.eval()
            running_loss = 0.0
            running_corrects = 0

            with torch.no_grad():
                for inputs, labels in dataloaders["valid"]:
                    inputs = inputs.to(device)
                    labels = labels.to(device)

                    # Forward pass
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)

                    # Loss
                    loss = criterion(outputs, labels)

                    # Per batch statistics
                    running_loss += loss.item() * inputs.size(0)
                    running_corrects += torch.sum(preds == labels).item()

            # Per epoch statistics
            val_loss = running_loss / dataset_sizes["valid"]
            val_acc = running_corrects / dataset_sizes["valid"]
            print(f"Valid Loss: {val_loss:.4f} Acc: {val_acc:.4f}")
            val_losses.append(val_loss)
            val_accs.append(val_acc)

            # Save best model
            if val_acc > best_acc:
                best_acc = val_acc
                torch.save(model.state_dict(), best_model_path)

            # Scheduler step for LR degradation
            scheduler.step()

    except KeyboardInterrupt:
        print("\nTraining interrupted by user!")

    finally:
        # Load best model
        if os.path.exists(best_model_path):
            model.load_state_dict(torch.load(best_model_path))
            print(f"Loaded best model with val acc: {best_acc:.4f}")
        else:
            print("No best model saved, using last epoch weights.")

        # Permanently save best model
        torch.save(model.state_dict(), os.path.join(final_model_path, "model.pt"))

        # Save training statistics
        history = {
            "train_loss": train_losses,
            "val_loss": val_losses,
            "train_acc": train_accs,
            "val_acc": val_accs,
        }
        with open(os.path.join(final_model_path, "statistics.json"), "w") as f:
            json.dump(history, f)

        time_elapsed = time.time() - since
        print(f'Training complete in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s')
        print(f'Best val Acc: {best_acc:.4f}')

    return model


def visualize_model(dataloaders, model, class_names, num_images=6):
    """Validate model and visualize with N images"""
    was_training = model.training
    model.eval()
    images_so_far = 0
    fig = plt.figure()

    with torch.no_grad():
        for i, (inputs, labels) in enumerate(dataloaders['valid']):
            inputs = inputs.to(device)
            labels = labels.to(device)

            # Forward pass
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)

            # Go through images and display
            for j in range(inputs.size()[0]):
                images_so_far += 1
                ax = plt.subplot(num_images//2, 2, images_so_far)
                ax.axis('off')
                ax.set_title(f'predicted: {class_names[preds[j]]}')
                imshow(inputs.cpu().data[j])

                if images_so_far == num_images:
                    model.train(mode=was_training)
                    return
        model.train(mode=was_training)

# Utils
def imshow(inp, title=None):
    """Display image for Tensor."""
    # Restructure and unnormalize
    inp = inp.numpy().transpose((1, 2, 0))
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    inp = std * inp + mean
    inp = np.clip(inp, 0, 1)

    # Display
    plt.imshow(inp)
    if title is not None:
        plt.title(title)
    plt.pause(0.001)

if __name__ == "__main__":
    # Device agnostic
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using {device} device")

    # Prepare dataloaders
    dataloaders, dataset_sizes, class_names = prepare_dataloaders(DATA_DIR)

    # Prepare model
    model_ft = timm.create_model(
        "resnet10t",
        pretrained=True,
        num_classes = 2
    )
    model_ft.to(device)

    # Prepare optimizer and loss
    criterion = nn.CrossEntropyLoss()
    optimizer_ft = optim.Adam(model_ft.parameters(), lr=LEARNING_RATE)
    exp_lr_scheduler = lr_scheduler.StepLR(optimizer_ft, step_size=7, gamma=0.1)

    # Train model
    model_ft = train_model(dataloaders, model_ft, criterion, optimizer_ft, exp_lr_scheduler, dataset_sizes, num_epochs=EPOCHS)

    # Visualize model
    visualize_model(dataloaders, model_ft, class_names)