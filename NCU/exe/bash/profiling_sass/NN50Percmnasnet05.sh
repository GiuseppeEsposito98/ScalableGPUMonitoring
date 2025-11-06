


ncu --csv --force-overwrite --log-file data/raw/ncu/NN50Percmnasnet05sass_1.csv \
        --print-source sass --page source --force-overwrite \
        --target-processes all --replay-mode kernel --kernel-name-base function --launch-skip-before-match 0 \
        --profile-from-start 1 --cache-control all --clock-control base --apply-rules yes    --import-source no \
        --check-exit-code yes \
        python3 /home/g.esposito/ScalableGPUMonitoring/NCU/test-apps/NNs/evaluate.py\
                --model_name mnasnet0_5 \
                --dataset_name CIFAR10 \
                --batch_size 10000 \
                --num_iterations 10000000000000000000 \
                --duration 300
