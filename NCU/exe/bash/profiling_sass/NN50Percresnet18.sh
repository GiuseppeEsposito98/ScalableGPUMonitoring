


ncu --csv --log-file data/raw/ncu/NN50Percresnet18sass_1.csv --print-source sass --page source --force-overwrite \
        --target-processes all --replay-mode kernel --kernel-name-base function --launch-skip-before-match 0 \
        --profile-from-start 1 --cache-control all --clock-control base --apply-rules yes    --import-source no \
        --check-exit-code yes \
        # this inferences should occupy 90% of the memory with an epsilon of 3391.5 MB for 1 hour
        python3 /home/bepi/Desktop/Ph.D_/projects/GPU_stress/code/ScalableGPUMonitoring/cupti/02_profiling_injection/test-apps/NNs/evaluate.py\
                --model_name resnet18 \
                --dataset_name CIFAR10 \
                --batch_size 4096 \
                --num_iterations 100 \
                --duration 350