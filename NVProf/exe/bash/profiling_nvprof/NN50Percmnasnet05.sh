#!/bin/bash
export PATH="/usr/local/cuda-12.6/bin:$PATH" 
export PATH="/home/bepi/anaconda3/bin:$PATH"
source /home/bepi/anaconda3/bin/activate
conda deactivate 

conda activate gpustress

ncu --export /home/bepi/Desktop/Ph.D_/projects/GPU_stress/code/ScalableGPUMonitoring/NCU/mnasnetreport.ncu-proj --force-overwrite --target-processes all --replay-mode kernel --kernel-name-base function --launch-skip-before-match 0 --section SpeedOfLight_RooflineChart --profile-from-start 1 --cache-control all --clock-control base --apply-rules yes --import-source no --check-exit-code yes python3 test-apps/NNs/evaluate.py\
        --model_name mnasnet0_5 \
        --dataset_name CIFAR10 \
        --batch_size 10000 \
        --num_iterations 100 \
        --duration 100
    