
echo $PWD
export LD_LIBRARY_PATH="/home/bepi/Desktop/Ph.D_/projects/GPU_stress/code/ScalableGPUMonitoring/cupti/01_pc_sampling_continuous/":"/usr/local/cuda-12/lib64"
data_folder_path="/home/bepi/Desktop/Ph.D_/projects/GPU_stress/code/ScalableGPUMonitoring/cupti/01_pc_sampling_continuous/data/Parallel"
./libpc_sampling_continuous.pl --collection-mode 1 --sampling-period 5 --file-name 5kernels_backprop.dat --app "./test-apps/gpu-rodinia/bin/linux/cuda/backprop 65536"

export LD_LIBRARY_PATH="/home/bepi/Desktop/Ph.D_/projects/GPU_stress/code/ScalableGPUMonitoring/cupti/01_pc_sampling_continuous/":"/usr/local/cuda-12/lib64"
./libpc_sampling_continuous.pl --collection-mode 1 --sampling-period 5 --file-name 5kernels_gaussian.dat --circular-buf-count 410 --app "./test-apps/gpu-rodinia/bin/linux/cuda/gaussian -f ./test-apps/gpu-rodinia/gaussian/matrix1024.txt"

export LD_LIBRARY_PATH="/home/bepi/Desktop/Ph.D_/projects/GPU_stress/code/ScalableGPUMonitoring/cupti/01_pc_sampling_continuous/":"/usr/local/cuda-12/lib64"
./libpc_sampling_continuous.pl --collection-mode 1 --sampling-period 5 --file-name 5kernels_sc_gpu.dat --app "./test-apps/gpu-rodinia/bin/linux/cuda/sc_gpu 0 10 256 1024 32 32 null out.txt 128"

export LD_LIBRARY_PATH="/home/bepi/Desktop/Ph.D_/projects/GPU_stress/code/ScalableGPUMonitoring/cupti/01_pc_sampling_continuous/":"/usr/local/cuda-12/lib64"
./libpc_sampling_continuous.pl --collection-mode 1 --sampling-period 5 --file-name 5kernels_srad_v2.dat --app "./test-apps/gpu-rodinia/bin/linux/cuda/srad_v2 2048 2048 50 60 50 60 0.2 5"

# export LD_LIBRARY_PATH="/home/bepi/Desktop/Ph.D_/projects/GPU_stress/code/ScalableGPUMonitoring/cupti/01_pc_sampling_continuous/":"/usr/local/cuda-12/lib64"
# ./libpc_sampling_continuous.pl --collection-mode 1 --sampling-period 30 --file-name 5kernels_gpuburn.dat --circular-buf-count 460 --hw-buf-size 1024 MB --app "./test-apps/gpu-burn/gpu_burn 60 -i 0 -c ./test-apps/gpu-burn/compare.ptx -m 50%"

export PATH="/home/bepi/anaconda3/bin:$PATH"
source /home/bepi/anaconda3/bin/activate
conda deactivate 

conda activate gpustress

./libpc_sampling_continuous.pl --collection-mode 1 --sampling-period 5 --file-name 5kernels_lenet5.dat --app "python3 /home/bepi/Desktop/Ph.D_/projects/GPU_stress/code/ScalableGPUMonitoring/cupti/01_pc_sampling_continuous/exe/LeNet5.py"

mv 5kernels_backprop.dat data/raw/Parallel/5_backprop.dat
mv 5kernels_gaussian.dat data/raw/Parallel/5_gaussian.dat
mv 5kernels_sc_gpu.dat data/raw/Parallel/5_sc_gpu.dat
mv 5kernels_srad_v2.dat data/raw/Parallel/5_srad_v2.dat
mv 5kernels_lenet5.dat data/raw/Parallel/5_lenet5.dat
mv 5kernels_gpuburn.dat data/raw/Parallel/5_gpuburn.dat





# export LD_LIBRARY_PATH="/home/bepi/Desktop/Ph.D_/projects/GPU_stress/code/ScalableGPUMonitoring/cupti/01_pc_sampling_continuous/":"/usr/local/cuda-12/lib64"
# ./libpc_sampling_continuous.pl --collection-mode 1 --sampling-period 5 --file-name 5kernels_heartwall.dat --app "./test-apps/gpu-rodinia/bin/linux/cuda/heartwall ./test-apps/gpu-rodinia/heartwall/test.avi 104"

# export LD_LIBRARY_PATH="/home/bepi/Desktop/Ph.D_/projects/GPU_stress/code/ScalableGPUMonitoring/cupti/01_pc_sampling_continuous/":"/usr/local/cuda-12/lib64"
# ./libpc_sampling_continuous.pl --collection-mode 1 --sampling-period 5 --file-name 5kernels_hotspot.dat --app "./test-apps/gpu-rodinia/bin/linux/cuda/hotspot 500 10 10 ./test-apps/gpu-rodinia/hotspot/temp_1024 ./test-apps/gpu-rodinia/hotspot/power_1024 out.txt"

# export LD_LIBRARY_PATH="/home/bepi/Desktop/Ph.D_/projects/GPU_stress/code/ScalableGPUMonitoring/cupti/01_pc_sampling_continuous/":"/usr/local/cuda-12/lib64"
# ./libpc_sampling_continuous.pl --collection-mode 1 --sampling-period 5 --file-name 5kernels_needle.dat --app "./test-apps/gpu-rodinia/bin/linux/cuda/needle 32768 0.1"