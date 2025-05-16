export PATH="/home/bepi/anaconda3/bin:$PATH"
source /home/bepi/anaconda3/bin/activate
conda deactivate 

conda activate gpustress

nsys profile \
    --output=reportNN.nsys-rep \
    --trace=cuda,nvtx \
    --gpu-metrics-device=all \
    --cuda-memory-usage=true \
    --cudabacktrace=true \
    --sampling-period=293750 \
    python3 test-apps/NNs/evaluate.py\
    --model_name mnasnet0_5 \
    --dataset_name CIFAR10 \
    --batch_size 10000 \
    --num_iterations 100 \
    --duration 100
    