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
# 
# ncu --set roofline \
#     --export report.ncu-rep \
#     --replay-mode application \
#     --app-replay-mode relaxed ./test-apps/gpu-burnCustom/gpu_burn -i 0 -c test-apps/gpu-burnCustom/compare.ptx -stts 60s 10 1
export PATH="/usr/local/cuda-12.6/bin:$PATH" 
ncu --export /home/bepi/Desktop/Ph.D_/projects/GPU_stress/code/ScalableGPUMonitoring/NCU/report.ncu-proj --force-overwrite --target-processes all --replay-mode kernel --kernel-name-base function --launch-skip-before-match 0 --section SpeedOfLight_RooflineChart --profile-from-start 1 --cache-control all --clock-control base --apply-rules yes --import-source no --check-exit-code yes /home/bepi/Desktop/Ph.D_/projects/GPU_stress/code/ScalableGPUMonitoring/NCU/test-apps/gpu-burn/gpu_burn -i 0 -c test-apps/gpu-burnCustom/compare.ptx -stts 60s 10 1