# import torch
# import torch.nn as nn
# import torch.optim as optim
# from torch.utils.data import DataLoader, random_split
# from dataset import StainMaskDataset
# from model import StainLevelModel

# # Config
# DATA_PATH = r"C:\Users\KIIT0001\Downloads\archive (1)\dataset"
# BATCH_SIZE = 32 
# LR = 1e-4
# EPOCHS = 10
# DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# def train():
#     full_dataset = StainMaskDataset(DATA_PATH)
    
#     if len(full_dataset) == 0:
#         print("❌ Dataset is empty. Check the console above for folder missing errors.")
#         return

#     # 80/20 Split
#     train_size = int(0.8 * len(full_dataset))
#     val_size = len(full_dataset) - train_size
#     train_ds, val_ds = random_split(full_dataset, [train_size, val_size])

#     train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, num_workers=2)
#     val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False)

#     model = StainLevelModel(num_classes=6).to(DEVICE)
#     criterion = nn.CrossEntropyLoss()
#     optimizer = optim.Adam(model.parameters(), lr=LR)

#     print(f"🚀 Training on {DEVICE} with {len(full_dataset)} total images...")

#     for epoch in range(EPOCHS):
#         model.train()
#         total_loss = 0
#         for x, y in train_loader:
#             x, y = x.to(DEVICE), y.to(DEVICE)
#             optimizer.zero_grad()
#             out = model(x)
#             loss = criterion(out, y)
#             loss.backward()
#             optimizer.step()
#             total_loss += loss.item()

#         # Validation
#         model.eval()
#         correct = 0
#         with torch.no_grad():
#             for x, y in val_loader:
#                 x, y = x.to(DEVICE), y.to(DEVICE)
#                 out = model(x)
#                 correct += (out.argmax(1) == y).sum().item()
        
#         acc = (correct / val_size) * 100
#         print(f"Epoch {epoch+1}/{EPOCHS} | Loss: {total_loss/len(train_loader):.4f} | Val Acc: {acc:.2f}%")

#     torch.save(model.state_dict(), "stain_model.pth")
#     print("✅ Model saved as stain_model.pth")

# if __name__ == "__main__":
#     train()

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from dataset import StainMaskDataset
from model import StainLevelModel
from tqdm import tqdm  # <--- New import

# Config
DATA_PATH = r"C:\Users\KIIT0001\Downloads\archive (1)\dataset\local_dataset"
BATCH_SIZE = 16   # Optimized for CPU cache
LR = 1e-4
EPOCHS = 10
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

def train():
    full_dataset = StainMaskDataset(DATA_PATH)
    
    if len(full_dataset) == 0:
        print("❌ Dataset is empty.")
        return

    # 80/20 Split
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_ds, val_ds = random_split(full_dataset, [train_size, val_size])

    # On CPU, num_workers=0 is often faster to avoid overhead
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False)

    model = StainLevelModel(num_classes=6).to(DEVICE)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LR)

    print(f"🚀 Training on {DEVICE} with {len(full_dataset)} images...")

    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0
        
        # Wrap the loader with tqdm for a progress bar
        loop = tqdm(train_loader, desc=f"Epoch {epoch+1}/{EPOCHS}", unit="batch")
        
        for x, y in loop:
            x, y = x.to(DEVICE), y.to(DEVICE)
            
            optimizer.zero_grad()
            out = model(x)
            loss = criterion(out, y)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
            # Update the progress bar with the current loss
            loop.set_postfix(loss=loss.item())

        # Validation
        model.eval()
        correct = 0
        with torch.no_grad():
            for x, y in val_loader:
                x, y = x.to(DEVICE), y.to(DEVICE)
                out = model(x)
                correct += (out.argmax(1) == y).sum().item()
        
        acc = (correct / val_size) * 100
        print(f"✨ Epoch {epoch+1} Complete | Avg Loss: {total_loss/len(train_loader):.4f} | Val Acc: {acc:.2f}%")

    torch.save(model.state_dict(), "stain_model.pth")
    print("✅ Model saved as stain_model.pth")

if __name__ == "__main__":
    train()