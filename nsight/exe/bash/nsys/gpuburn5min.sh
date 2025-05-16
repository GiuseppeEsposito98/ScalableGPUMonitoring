# dir=`pwd`
# shared_folder="$dir/shared"
# echo "Folder for storing results: $shared_folder"
# echo "Starting to profile the applications"

# Outer loop goes through the sequence 1, 2, 4, 8, 16, 32
# for memory in 16 32; do
#     echo "Profiling the apps using $i number elements inside the shared memory"
#     profile_file="$shared_folder/$size/$memory/report.nsys-rep"
    # command="nsys profile \
    #  --output=$profile_file --trace=cuda,osrt,nvtx \
    #  --cuda-memory-usage=true \
    #  --gpu-metrics-device=all \
    #  --capture-range=cudaProfilerApi \
    #  --cudabacktrace=true \
    #  test-apps/gpu-burn/gpu_burn $size $memory"

nsys profile \
    --output=reportNN.nsys-rep \
    --trace=cuda,nvtx \
    --gpu-metrics-device=all \
    --cuda-memory-usage=true \
    --cudabacktrace=true \
    --sampling-period=293750 \
    ./test-apps/gpu-burnCustom/gpu_burn \
    -i 0 \
    -c ./test-apps/gpu-burnCustom/compare.ptx \
    -m 50% \
    10