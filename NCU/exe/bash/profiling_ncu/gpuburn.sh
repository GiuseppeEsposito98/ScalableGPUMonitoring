echo ${PWD}

mkdir data 
mkdir data/postprocessed
mkdir data/postprocessed/ncu

mkdir data/raw
mkdir data/raw/ncu

export PATH="/usr/local/cuda-11.6/bin:$PATH" 
# --devices "0,1"
nv-nsight-cu-cli --csv \
    --log-file data/raw/ncu/report.csv --force-overwrite  \
    --target-processes all --replay-mode kernel --kernel-name-base function --launch-skip-before-match 0 \
    --section MemoryWorkloadAnalysis --section ComputeWorkloadAnalysis --section WarpStateStats \
    --profile-from-start 1 --cache-control all --clock-control base --apply-rules yes\
    --import-source no --check-exit-code yes \
    test-apps/gpu-burn/gpu_burn -m 95%\
    -c test-apps/gpu-burn/compare.ptx 10 