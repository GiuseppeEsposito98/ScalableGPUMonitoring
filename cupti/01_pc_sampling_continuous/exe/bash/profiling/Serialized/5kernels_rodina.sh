
echo $PWD
export LD_LIBRARY_PATH="/home/bepi/Desktop/Ph.D_/projects/GPU_stress/code/ScalableGPUMonitoring/cupti/01_pc_sampling_continuous/":"/usr/local/cuda-12/lib64"
data_folder_path="/home/bepi/Desktop/Ph.D_/projects/GPU_stress/code/ScalableGPUMonitoring/cupti/01_pc_sampling_continuous/data/Parallel"
./libpc_sampling_continuous.pl --collection-mode 2 --sampling-period 5 --file-name 5kernels_backprop.dat --app "./test-apps/gpu-rodinia/bin/linux/cuda/backprop 65536"

export LD_LIBRARY_PATH="/home/bepi/Desktop/Ph.D_/projects/GPU_stress/code/ScalableGPUMonitoring/cupti/01_pc_sampling_continuous/":"/usr/local/cuda-12/lib64"
./libpc_sampling_continuous.pl --collection-mode 2 --sampling-period 5 --file-name 5kernels_gaussian.dat --circular-buf-count 390 --app "./test-apps/gpu-rodinia/bin/linux/cuda/gaussian -f ./test-apps/gpu-rodinia/gaussian/matrix1024.txt"

export LD_LIBRARY_PATH="/home/bepi/Desktop/Ph.D_/projects/GPU_stress/code/ScalableGPUMonitoring/cupti/01_pc_sampling_continuous/":"/usr/local/cuda-12/lib64"
./libpc_sampling_continuous.pl --collection-mode 2 --sampling-period 5 --file-name 5kernels_sc_gpu.dat --app "./test-apps/gpu-rodinia/bin/linux/cuda/sc_gpu 0 10 256 1024 32 32 null out.txt 128"

export LD_LIBRARY_PATH="/home/bepi/Desktop/Ph.D_/projects/GPU_stress/code/ScalableGPUMonitoring/cupti/01_pc_sampling_continuous/":"/usr/local/cuda-12/lib64"
./libpc_sampling_continuous.pl --collection-mode 2 --sampling-period 5 --file-name 5kernels_srad_v2.dat --app "./test-apps/gpu-rodinia/bin/linux/cuda/srad_v2 2048 2048 50 60 50 60 0.5 20"

# export LD_LIBRARY_PATH="/home/bepi/Desktop/Ph.D_/projects/GPU_stress/code/ScalableGPUMonitoring/cupti/01_pc_sampling_continuous/":"/usr/local/cuda-12/lib64"
# ./libpc_sampling_continuous.pl --collection-mode 2 --sampling-period 5 --file-name 5kernels_gpuburn.dat --app "./test-apps/gpu-burn/gpu_burn 60"

export PATH="/home/bepi/anaconda3/bin:$PATH"
source /home/bepi/anaconda3/bin/activate
conda deactivate 

conda activate gpustress

./libpc_sampling_continuous.pl --collection-mode 2 --sampling-period 5 --file-name 5kernels_lenet5.dat --app "python3 /home/bepi/Desktop/Ph.D_/projects/GPU_stress/code/ScalableGPUMonitoring/cupti/01_pc_sampling_continuous/exe/LeNet5.py"

mv 1_5kernels_backprop.dat data/raw/Serialized/1_5_backprop.dat
mv 1_5kernels_gaussian.dat data/raw/Serialized/1_5_gaussian.dat
mv 1_5kernels_sc_gpu.dat data/raw/Serialized/1_5_sc_gpu.dat
mv 1_5kernels_srad_v2.dat data/raw/Serialized/1_5_srad_v2.dat
mv 1_5kernels_lenet5.dat data/raw/Serialized/1_5_lenet5.dat
# mv 5kernels_gpuburn.dat data/raw/Parallel/5_gpuburn.dat

