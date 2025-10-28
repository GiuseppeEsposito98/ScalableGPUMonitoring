# Instructions to run the training with different settings

### Resnet50 for classification on CIFAR10 dataset

- **Collect checkpoints at each epoch** and check the training algorithm convergence without profiling 
```bash
python train.py --task classification --model resnet50 --dataset cifar10 --num_classes 10 --epochs 20 --lr 0.001 --resume_checkpoint "" --batch_size 32 --profile_target None --layer_profile_target None --profile_duration None --extract_frequent_checkpoints True
```

- **Continue training from a checkpoint** and check the training algorithm convergence without profiling
```bash
python train.py --task classification --model resnet50 --dataset cifar10 --num_classes 10 --epochs 20 --lr 0.001 --resume_checkpoint "path_to_ckpt" --batch_size 32 --profile_target None --layer_profile_target None --profile_duration None --extract_frequent_checkpoints True
```

- **Profile the forward** starting from a specific checkpoint of the model as a whole (not targeting a specific layer)
```bash
python train.py --task classification --model resnet50 --dataset cifar10 --num_classes 10 --epochs 20 --lr 0.001 --resume_checkpoint "path_to_ckpt" --batch_size 32 --profile_target "forward" --layer_profile_target None --profile_duration None --extract_frequent_checkpoints False
```
- **Profile the loss** starting from a specific checkpoint of the model as a whole (not targeting a specific layer)
```bash
python train.py --task classification --model resnet50 --dataset cifar10 --num_classes 10 --epochs 20 --lr 0.001 --resume_checkpoint "path_to_ckpt" --batch_size 32 --profile_target "loss" --layer_profile_target None --profile_duration None --extract_frequent_checkpoints False
```
- **Profile the backward** starting from a specific checkpoint of the model as a whole (not targeting a specific layer)
```bash
python train.py --task classification --model resnet50 --dataset cifar10 --num_classes 10 --epochs 20 --lr 0.001 --resume_checkpoint "path_to_ckpt" --batch_size 32 --profile_target "backward" --layer_profile_target None --profile_duration None --extract_frequent_checkpoints False

- **Profile the optimizer_step** starting from a specific checkpoint of the model as a whole (not targeting a specific layer)
```bash
python train.py --task classification --model resnet50 --dataset cifar10 --num_classes 10 --epochs 20 --lr 0.001 --resume_checkpoint "path_to_ckpt" --batch_size 32 --profile_target "optimizer_step" --layer_profile_target None --profile_duration None --extract_frequent_checkpoints False
```
### Mobilenet-V3 for classification on CIFAR10 dataset

- **Collect checkpoints at each epoch** and check the training algorithm convergence without profiling 
```bash
python train.py --task classification --model mobilenetv3 --dataset cifar10 --num_classes 10 --epochs 20 --lr 0.001 --resume_checkpoint "" --batch_size 32 --profile_target None --layer_profile_target None --profile_duration None --extract_frequent_checkpoints True
```
- **Continue training from a checkpoint** and check the training algorithm convergence without profiling
```bash
python train.py --task classification --model mobilenetv3 --dataset cifar10 --num_classes 10 --epochs 20 --lr 0.001 --resume_checkpoint "path_to_ckpt" --batch_size 32 --profile_target None --layer_profile_target None --profile_duration None --extract_frequent_checkpoints True
```
- **Profile the forward** starting from a specific checkpoint of the model as a whole (not targeting a specific layer)
```bash
python train.py --task classification --model mobilenetv3 --dataset cifar10 --num_classes 10 --epochs 20 --lr 0.001 --resume_checkpoint "path_to_ckpt" --batch_size 32 --profile_target "forward" --layer_profile_target None --profile_duration None --extract_frequent_checkpoints False
```
- **Profile the loss** starting from a specific checkpoint of the model as a whole (not targeting a specific layer)
```bash
python train.py --task classification --model mobilenetv3 --dataset cifar10 --num_classes 10 --epochs 20 --lr 0.001 --resume_checkpoint "path_to_ckpt" --batch_size 32 --profile_target "loss" --layer_profile_target None --profile_duration None --extract_frequent_checkpoints False
```
- **Profile the backward** starting from a specific checkpoint of the model as a whole (not targeting a specific layer)
```bash
python train.py --task classification --model mobilenetv3 --dataset cifar10 --num_classes 10 --epochs 20 --lr 0.001 --resume_checkpoint "path_to_ckpt" --batch_size 32 --profile_target "backward" --layer_profile_target None --profile_duration None --extract_frequent_checkpoints False
```
- **Profile the optimizer_step** starting from a specific checkpoint of the model as a whole (not targeting a specific layer)
```bash
python train.py --task classification --model mobilenetv3 --dataset cifar10 --num_classes 10 --epochs 20 --lr 0.001 --resume_checkpoint "path_to_ckpt" --batch_size 32 --profile_target "optimizer_step" --layer_profile_target None --profile_duration None --extract_frequent_checkpoints False
```
### Vision Transformer for classification on CIFAR10 dataset

- **Collect checkpoints at each epoch** and check the training algorithm convergence without profiling 
```bash
python train.py --task classification --model vit --dataset cifar10 --num_classes 10 --epochs 20 --lr 0.001 --resume_checkpoint "" --batch_size 32 --profile_target None --layer_profile_target None --profile_duration None --extract_frequent_checkpoints True
```
- **Continue training from a checkpoint** and check the training algorithm convergence without profiling
```bash
python train.py --task classification --model vit --dataset cifar10 --num_classes 10 --epochs 20 --lr 0.001 --resume_checkpoint "path_to_ckpt" --batch_size 32 --profile_target None --layer_profile_target None --profile_duration None --extract_frequent_checkpoints True
```
- **Profile the forward** starting from a specific checkpoint of the model as a whole (not targeting a specific layer)
```bash
python train.py --task classification --model vit --dataset cifar10 --num_classes 10 --epochs 20 --lr 0.001 --resume_checkpoint "path_to_ckpt" --batch_size 32 --profile_target "forward" --layer_profile_target None --profile_duration None --extract_frequent_checkpoints False
```
- **Profile the loss** starting from a specific checkpoint of the model as a whole (not targeting a specific layer)
```bash
python train.py --task classification --model vit --dataset cifar10 --num_classes 10 --epochs 20 --lr 0.001 --resume_checkpoint "path_to_ckpt" --batch_size 32 --profile_target "loss" --layer_profile_target None --profile_duration None --extract_frequent_checkpoints False
```
- **Profile the backward** starting from a specific checkpoint of the model as a whole (not targeting a specific layer)
```bash
python train.py --task classification --model vit --dataset cifar10 --num_classes 10 --epochs 20 --lr 0.001 --resume_checkpoint "path_to_ckpt" --batch_size 32 --profile_target "backward" --layer_profile_target None --profile_duration None --extract_frequent_checkpoints False
```
- **Profile the optimizer_step** starting from a specific checkpoint of the model as a whole (not targeting a specific layer)
```bash
python train.py --task classification --model vit --dataset cifar10 --num_classes 10 --epochs 20 --lr 0.001 --resume_checkpoint "path_to_ckpt" --batch_size 32 --profile_target "optimizer_step" --layer_profile_target None --profile_duration None --extract_frequent_checkpoints False
```
### DeepLab-V3 for semantic segmentation on Pascal VOC dataset

- **Collect checkpoints at each epoch** and check the training algorithm convergence without profiling 
```bash
python train.py --task segmentation --model deeplabv3 --data_dir ~/dataset/VOC --num_classes 20 --epochs 20 --lr 0.001 --resume_checkpoint "" --batch_size 32 --profile_target None --layer_profile_target None --profile_duration None --extract_frequent_checkpoints True
```
- **Continue training from a checkpoint** and check the training algorithm convergence without profiling
```bash
python train.py --task segmentation --model deeplabv3 --data_dir ~/dataset/VOC --num_classes 20 --epochs 20 --lr 0.001 --resume_checkpoint "path_to_ckpt" --batch_size 32 --profile_target None --layer_profile_target None --profile_duration None --extract_frequent_checkpoints True
```
- **Profile the forward** starting from a specific checkpoint of the model as a whole (not targeting a specific layer)
```bash
python train.py --task segmentation --model deeplabv3 --data_dir ~/dataset/VOC --num_classes 20 --epochs 20 --lr 0.001 --resume_checkpoint "path_to_ckpt" --batch_size 32 --profile_target "forward" --layer_profile_target None --profile_duration None --extract_frequent_checkpoints False
```
- **Profile the loss** starting from a specific checkpoint of the model as a whole (not targeting a specific layer)
```bash
python train.py --task segmentation --model deeplabv3 --data_dir ~/dataset/VOC --num_classes 20 --epochs 20 --lr 0.001 --resume_checkpoint "path_to_ckpt" --batch_size 32 --profile_target "loss" --layer_profile_target None --profile_duration None --extract_frequent_checkpoints False
```
- **Profile the backward** starting from a specific checkpoint of the model as a whole (not targeting a specific layer)
```bash
python train.py --task segmentation --model deeplabv3 --data_dir ~/dataset/VOC --num_classes 20 --epochs 20 --lr 0.001 --resume_checkpoint "path_to_ckpt" --batch_size 32 --profile_target "backward" --layer_profile_target None --profile_duration None --extract_frequent_checkpoints False
```
- **Profile the optimizer_step** starting from a specific checkpoint of the model as a whole (not targeting a specific layer)
```bash
python train.py --task segmentation --model deeplabv3 --data_dir ~/dataset/VOC --num_classes 20 --epochs 20 --lr 0.001 --resume_checkpoint "path_to_ckpt" --batch_size 32 --profile_target "optimizer_step" --layer_profile_target None --profile_duration None --extract_frequent_checkpoints False
```