from PIL import Image
import numpy as np
import torch
from torchvision import models
from torch import nn
import time
# -----------------------------
# Utility Functions
# -----------------------------
def visualize_segmentation(pred, img):
    pred = torch.argmax(pred.squeeze(), dim=0).cpu().numpy()
    # Simple color mapping
    colors = np.array([[0,0,0],[255,0,0],[0,255,0],[0,0,255],[255,255,0],[255,0,255],[0,255,255]], dtype=np.uint8)
    mask = colors[pred % len(colors)]
    return Image.fromarray(mask)

def validate_classification(model, val_loader, device):
    model.eval()
    correct, total, val_loss = 0, 0, 0.0
    criterion = nn.CrossEntropyLoss()
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            val_loss += loss.item()
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    return val_loss / len(val_loader), correct / total


def get_classification_model(model_name, num_classes):
    if model_name == "mobilenetv3":
        model = models.mobilenet_v3_large(weights=None)
        model.classifier[3] = nn.Linear(model.classifier[3].in_features, num_classes)
    elif model_name == "resnet50":
        model = models.resnet50(weights=None)
        model.fc = nn.Linear(model.fc.in_features, num_classes)
    elif model_name == "vit":
        model = models.vit_b_16(weights=None)
        model.heads.head = nn.Linear(model.heads.head.in_features, num_classes)
    else:
        raise ValueError("Unsupported model for classification")
    return model

def get_segmentation_model(model_name, num_classes):
    if model_name == "deeplabv3":
        model = models.segmentation.deeplabv3_resnet50(weights=None)
        model.classifier[4] = nn.Conv2d(model.classifier[4].in_channels, num_classes, kernel_size=1)
    else:
        raise ValueError("Unsupported segmentation model")
    return model


def validate_segmentation(model, val_loader, device):
    model.eval()
    criterion = nn.CrossEntropyLoss()
    val_loss = 0.0
    iou_total = 0.0
    with torch.no_grad():
        for images, targets in val_loader:
            images = images.to(device)
            targets = targets["segmentation"].to(device)
            outputs = model(images)["out"]
            loss = criterion(outputs, targets)
            val_loss += loss.item()
            preds = torch.argmax(outputs, dim=1)
            intersection = (preds & targets).float().sum((1,2))
            union = (preds | targets).float().sum((1,2))
            iou = (intersection / (union + 1e-6)).mean().item()
            iou_total += iou
    return val_loss / len(val_loader), iou_total / len(val_loader)

def is_end(start, max_duration):
    end = time.time()
    duration = end - start
    if duration < max_duration:
        return True
    else:
        return False