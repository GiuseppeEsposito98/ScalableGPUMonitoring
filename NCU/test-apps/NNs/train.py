import argparse
import os
import torch
from torchvision import transforms, datasets, models
from torch import nn, optim
from torch.utils.tensorboard import SummaryWriter
from ultralytics import YOLO
from utils import validate_segmentation, get_classification_model, validate_classification, visualize_segmentation, is_end, get_segmentation_model
import time
import sys

# -----------------------------
# CLASSIFICATION TRAINING
# -----------------------------
def train_classification(model_name, 
                        dataset_name, 
                        num_classes, 
                        epochs=10, 
                        lr=0.001, 
                        resume_checkpoint=None, 
                        batch_size=32,
                        extract_frequent_checkpoints=False,
                        profile_target=None,
                        profile_duration=None,
                        layer_profile_target=None):
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if not extract_frequent_checkpoints:
        writer = SummaryWriter(log_dir=f"runs/{model_name}_classification")

    # Get model without pretrained weights
    model = get_classification_model(model_name, num_classes).to(device)

    optimizer = optim.Adam(model.parameters(), lr=lr)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)

    start_epoch = 0
    best_acc = 0.0

    # Resume from checkpoint if provided
    if resume_checkpoint and os.path.isfile(resume_checkpoint):
        print(f"Resuming training from checkpoint: {resume_checkpoint}")
        checkpoint = torch.load(resume_checkpoint, map_location=device)
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
        start_epoch = checkpoint['epoch'] + 1
        best_acc = checkpoint.get('best_acc', 0.0)

    # CIFAR transforms
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    # Load CIFAR dataset
    if dataset_name.lower() == "cifar10":
        train_dataset = datasets.CIFAR10(root="~/dataset/cifar10/", train=True, download=True, transform=transform)
        val_dataset = datasets.CIFAR10(root="~/dataset/cifar10/", train=False, download=True, transform=transform)
    elif dataset_name.lower() == "cifar100":
        train_dataset = datasets.CIFAR100(root="~/dataset/cifar100/", train=True, download=True, transform=transform)
        val_dataset = datasets.CIFAR100(root="~/dataset/cifar100/", train=False, download=True, transform=transform)
    else:
        raise ValueError("Unsupported dataset. Use cifar10 or cifar100.")

    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=batch_size)

    criterion = nn.CrossEntropyLoss()

    for epoch in range(start_epoch, epochs):
        print(f"Starting epoch {epoch+1}/{epochs}")
        model.train()
        running_loss = 0.0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()

            if profile_target == "forward":
                start = time.time()
                while not is_end(start, profile_duration):
                    outputs = model(images)
                sys.exit(0)
            outputs = model(images)

            if profile_target == "loss":
                start = time.time()
                while not is_end(start, profile_duration):
                    loss = criterion(outputs, labels)
                sys.exit(0)
            loss = criterion(outputs, labels)

            if profile_target == "backward":
                start = time.time()
                while not is_end(start, profile_duration):
                    loss.backward()
                sys.exit(0)
            loss.backward()

            if profile_target == "optimizer_step":
                start = time.time()
                while not is_end(start, profile_duration):
                    optimizer.step()
                sys.exit(0)
            optimizer.step()

            running_loss += loss.item()

        train_loss = running_loss / len(train_loader)
        val_loss, val_acc = validate_classification(model, val_loader, device)

        if not extract_frequent_checkpoints:
            # TensorBoard logging
            writer.add_scalar("Loss/train", train_loss, epoch)
            writer.add_scalar("Loss/val", val_loss, epoch)
            writer.add_scalar("Accuracy/val", val_acc, epoch)
            writer.add_scalar("LearningRate", scheduler.get_last_lr()[0], epoch)

        print(f"Epoch {epoch+1}/{epochs} | Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.4f}")
        if extract_frequent_checkpoints or epoch==epochs:
            # Save checkpoint at every epoch
            if not os.path.exists(f"./test_apps/NNs/checkpoints/{model_name}"):
                os.makedirs(f"./test_apps/NNs/checkpoints/{model_name}")
            checkpoint_path = f"{dataset_name}_epoch{epoch+1}.pth"
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'scheduler_state_dict': scheduler.state_dict(),
                'curr_acc': val_acc
            }, checkpoint_path)

        if val_acc > best_acc:
            best_acc = val_acc

        scheduler.step()
    if not extract_frequent_checkpoints:
        writer.close()
    return val_loader

# -----------------------------
# OBJECT DETECTION (YOLOv8)
# -----------------------------
def train_detection_yolo(data_yaml, epochs=50, batch_size=16):
    model = YOLO("yolov8n.pt")
    model.train(data=data_yaml, epochs=epochs, project="runs/yolo", name="exp", batch=batch_size, device='cuda' if torch.cuda.is_available() else "cpu")
    results = model.val()
    print("Detection validation results:", results)

# -----------------------------
# SEMANTIC SEGMENTATION
# -----------------------------

def train_segmentation(model_name, 
                        data_dir, 
                        num_classes, 
                        epochs=10, 
                        lr=0.001, 
                        resume_checkpoint=None, 
                        batch_size=4,
                        extract_frequent_checkpoints=False,
                        profile_target=None,
                        profile_duration=None,
                        layer_profile_target=None):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if not extract_frequent_checkpoints:
        writer = SummaryWriter(log_dir=f"runs/{model_name}_segmentation")

    model = get_segmentation_model(model_name, num_classes).to(device)

    optimizer = optim.Adam(model.parameters(), lr=lr)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)

    start_epoch = 0
    best_iou = 0.0

    # Resume from checkpoint if provided
    if resume_checkpoint and os.path.isfile(resume_checkpoint):
        print(f"Resuming training from checkpoint: {resume_checkpoint}")
        checkpoint = torch.load(resume_checkpoint, map_location=device)
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
        start_epoch = checkpoint['epoch'] + 1
        best_iou = checkpoint.get('best_iou', 0.0)

    transform = transforms.Compose([
        transforms.Resize((520, 520)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    train_dataset = datasets.VOCSegmentation(root=data_dir, year="2012", image_set="train", download=False, transform=transform)
    val_dataset = datasets.VOCSegmentation(root=data_dir, year="2012", image_set="val", download=False, transform=transform)

    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=batch_size)

    criterion = nn.CrossEntropyLoss()

    for epoch in range(start_epoch, epochs):
        model.train()
        running_loss = 0.0
        for images, targets in train_loader:
            images = images.to(device)
            targets = targets["segmentation"].to(device)
            optimizer.zero_grad()
            if profile_target == "forward":
                start = time.time()
                while not is_end(start, profile_duration):
                    outputs = model(images)["out"]
                sys.exit(0)
            outputs = model(images)["out"]

            if profile_target == "loss":
                start = time.time()
                while not is_end(start, profile_duration):
                    loss = criterion(outputs, targets)
                sys.exit(0)
            loss = criterion(outputs, targets)

            if profile_target == "backward":
                start = time.time()
                while not is_end(start, profile_duration):
                    loss.backward()
                sys.exit(0)
            loss.backward()

            if profile_target == "optimizer_step":
                start = time.time()
                while not is_end(start, profile_duration):
                    optimizer.step()
                sys.exit(0)
            optimizer.step()
            running_loss += loss.item()

        train_loss = running_loss / len(train_loader)
        val_loss, val_iou = validate_segmentation(model, val_loader, device)

        if not extract_frequent_checkpoints:
            writer.add_scalar("Loss/train", train_loss, epoch)
            writer.add_scalar("Loss/val", val_loss, epoch)
            writer.add_scalar("IoU/val", val_iou, epoch)
            writer.add_scalar("LearningRate", scheduler.get_last_lr()[0], epoch)

        sample_img, _ = next(iter(val_loader))
        sample_img = sample_img.to(device)
        with torch.no_grad():
            pred = model(sample_img)["out"]
        mask_img = visualize_segmentation(pred, sample_img)

        if not extract_frequent_checkpoints:
            writer.add_image("SamplePrediction", transforms.ToTensor()(mask_img), epoch)

        print(f"Epoch {epoch+1}/{epochs} | Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f} | Val IoU: {val_iou:.4f}")

        # Save checkpoint at every epoch
        if extract_frequent_checkpoints or epoch==epochs:
            # Save checkpoint at every epoch
            if not os.path.exists(f"./test_apps/NNs/checkpoints/{model_name}"):
                os.makedirs(f"./test_apps/NNs/checkpoints/{model_name}")

            checkpoint_path = f"{model_name}_epoch{epoch+1}.pth"
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'scheduler_state_dict': scheduler.state_dict(),
                'best_iou': best_iou
            }, checkpoint_path)

            if val_iou > best_iou:
                best_iou = val_iou
                torch.save(model.state_dict(), f"{model_name}_best.pth")

        scheduler.step()
    if not extract_frequent_checkpoints:
        writer.close()

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=["classification", "detection", "segmentation"], required=True)
    parser.add_argument("--model", type=str, required=False)
    parser.add_argument("--dataset", type=str, required=False)
    parser.add_argument("--data_dir", type=str, required=False)
    parser.add_argument("--num_classes", type=int, required=False)
    parser.add_argument("--data_yaml", type=str, required=False)
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--lr", type=float, default=0.001)
    parser.add_argument("--resume_checkpoint", type=str, default=None)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--profile_target", type=str, required=False)
    parser.add_argument("--layer_profile_target", type=str, required=False)
    parser.add_argument("--profile_duration", type=int, required=False)
    parser.add_argument("--extract_frequent_checkpoints", type=bool, default=False)
    args = parser.parse_args()

    if args.task == "classification":
        train_classification(args.model, 
                             args.dataset, 
                             args.num_classes, 
                             epochs=args.epochs, 
                             lr=args.lr,
                             resume_checkpoint=args.resume_checkpoint,
                             extract_frequent_checkpoints=args.extract_frequent_checkpoints,
                             profile_target=args.profile_target,
                             profile_duration=args.profile_duration,
                             layer_profile_target=args.layer_profile_target)
    # elif args.task == "detection":
    #     train_detection_yolo(args.data_yaml, epochs=args.epochs)
    elif args.task == "segmentation":
        train_segmentation(args.model, 
                           args.data_dir, 
                           args.num_classes, 
                           epochs=args.epochs, 
                           lr=args.lr,
                           resume_checkpoint=args.resume_checkpoint, 
                           extract_frequent_checkpoints=args.extract_frequent_checkpoints,
                           profile_target=args.profile_target,
                           profile_duration=args.profile_duration,
                           layer_profile_target=args.layer_profile_target)