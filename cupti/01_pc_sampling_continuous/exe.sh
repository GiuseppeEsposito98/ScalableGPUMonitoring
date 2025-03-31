echo $PWD
export LD_LIBRARY_PATH="/home/bepi/Desktop/Ph.D_/projects/GPU_stress/code/ScalableGPUMonitoring/cupti/01_pc_sampling_continuous/":"/usr/local/cuda-12/lib64"
./libpc_sampling_continuous.pl --collection-mode 1 --sampling-period 5 --file-name pcsampling.dat --app "./test-apps/vectoradd/vectoradd"