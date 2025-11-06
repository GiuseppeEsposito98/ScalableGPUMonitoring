
import torch, os
print("torch.cuda.is_available:", torch.cuda.is_available())
print("device count:", torch.cuda.device_count())
x = torch.rand(1, device="cuda")  # deve creare un contesto
torch.cuda.synchronize()
print("OK, contesto CUDA creato")
    