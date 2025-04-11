import torch
import torch.nn as nn
import torchvision
import torch
import torch.nn as nn
import torchvision.transforms as transforms
import os


# Defining the convolutional neural network
class LeNet5(nn.Module):
    def __init__(self, num_classes):
        super(LeNet5, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(1, 6, kernel_size=5, stride=1, padding=0),
            nn.BatchNorm2d(6),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.layer2 = nn.Sequential(
            nn.Conv2d(6, 16, kernel_size=5, stride=1, padding=0),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.fc = nn.Linear(400, 120)
        self.relu = nn.ReLU()
        self.fc1 = nn.Linear(120, 84)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(84, num_classes)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = out.reshape(out.size(0), -1)
        out = self.fc(out)
        out = self.relu(out)
        out = self.fc1(out)
        out = self.relu1(out)
        out = self.fc2(out)
        out = self.softmax(out)
        return out


def main():

    path = os.path.dirname(__file__)

    batch_size = 4

    LeNet_dict = {
        0: "zero",
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
    }

    # Device will determine whether to run the training on GPU or CPU.
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    

    test_dataset = torchvision.datasets.MNIST(
        root=os.path.join(path, "data"),
        train=False,
        transform=transforms.Compose(
            [
                transforms.Resize((32, 32)),
                transforms.ToTensor(),
                transforms.Normalize(mean=(0.1325,), std=(0.3105,)),
            ]
        ),
        download=True,
    )
    test_loader = torch.utils.data.DataLoader(
        dataset=test_dataset, batch_size=batch_size, shuffle=False
    )

    model = LeNet5(10)
    
    # model.load_state_dict(
    #     torch.load(
    #         os.path.join(path, "checkpoints/LeNet"), map_location=torch.device("cpu")
    #     )
    # )
    model = model.to(device)
    model.eval()


    with torch.no_grad():
        correct = 0
        total = 0
        img_idx = 0
        for batch, (images, labels) in enumerate(test_loader):
            images = images.to(device)                
            labels = labels.to(device)
            # if(labels[0].item()==0):
            model(images)
            img_idx+=1
            if img_idx == 32:
                break
            print(labels)
            

    
if __name__ == "__main__":
    main()