import torch
import torch.nn as nn
from torchvision import models

class StainLevelModel(nn.Module):
    def __init__(self, num_classes=6):
        super().__init__()
        # Load weights
        self.net = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)

        # Modify first layer: 3 channels (RGB) -> 4 channels (RGB + Mask)
        old_weights = self.net.conv1.weight.data
        self.net.conv1 = nn.Conv2d(4, 64, kernel_size=7, stride=2, padding=3, bias=False)
        
        with torch.no_grad():
            self.net.conv1.weight[:, :3, :, :] = old_weights
            self.net.conv1.weight[:, 3, :, :] = old_weights.mean(dim=1)

        # Output layer for 6 classes
        self.net.fc = nn.Linear(self.net.fc.in_features, num_classes)

    def forward(self, x):
        return self.net(x)