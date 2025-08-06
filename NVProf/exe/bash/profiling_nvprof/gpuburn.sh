echo ${PWD}

mkdir data 
mkdir data/postprocessed
mkdir data/postprocessed/nvprof

mkdir data/raw
mkdir data/raw/ncu
echo 'Ciao'
export PATH="/usr/local/cuda-11.6/bin:$PATH" 
# --devices "0,1"
nvprof --csv \
       --log-file data/raw/ncu/report.csv \
       --metrics all \
       --profile-child-processes \
       test-apps/gpu-burn/gpu_burn -m 95% -c test-apps/gpu-burn/compare.ptx 86400