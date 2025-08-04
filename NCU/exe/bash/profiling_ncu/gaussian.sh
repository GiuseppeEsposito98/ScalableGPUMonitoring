#!/bin/bash
export PATH="/usr/local/cuda-12.6/bin:$PATH" 

ncu --export /home/bepi/Desktop/Ph.D_/projects/GPU_stress/code/ScalableGPUMonitoring/NCU/gaussianreport.ncu-proj --force-overwrite --target-processes all --replay-mode kernel --kernel-name-base function --launch-skip-before-match 0 --section SpeedOfLight_RooflineChart --profile-from-start 1 --cache-control all --clock-control base --apply-rules yes --import-source no --check-exit-code yes \
    ./test-apps/gpu-rodinia/bin/linux/cuda/gaussian -f ./test-apps/gpu-rodinia/gaussian/matrix1024.txt