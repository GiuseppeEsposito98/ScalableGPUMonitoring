export INJECTION_KERNEL_COUNT=$1

export INJECTION_METRICS="gpc__cycles_elapsed.avg.per_second "
export INJECTION_METRICS=$INJECTION_METRICS"gr__cycles_active.sum.pct_of_peak_sustained_elapsed "
export INJECTION_METRICS=$INJECTION_METRICS"tpc__warps_active_realtime.avg.pct_of_peak_sustained_elapsed "
export INJECTION_METRICS=$INJECTION_METRICS"sm__cycles_active.avg.pct_of_peak_sustained_elapsed "
export INJECTION_METRICS=$INJECTION_METRICS"sm__inst_executed.avg.pct_of_peak_sustained_elapsed "
export INJECTION_METRICS=$INJECTION_METRICS"sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_elapsed "
export INJECTION_METRICS=$INJECTION_METRICS"dramc__sectors_op_read.avg.pct_of_peak_sustained_elapsed "
export INJECTION_METRICS=$INJECTION_METRICS"dramc__sectors_op_write.avg.pct_of_peak_sustained_elapsed "
export INJECTION_METRICS=$INJECTION_METRICS"pcie__read_bytes.avg.pct_of_peak_sustained_elapsed "
export INJECTION_METRICS=$INJECTION_METRICS"pcie__write_bytes.avg.pct_of_peak_sustained_elapsed "
export INJECTION_METRICS=$INJECTION_METRICS"pcie__read_bytes.sum  "
export INJECTION_METRICS=$INJECTION_METRICS"pcie__write_bytes.sum "

export PATH="/home/bepi/anaconda3/bin:$PATH"
source /home/bepi/anaconda3/bin/activate
conda deactivate 

conda activate gpustress

env CUDA_INJECTION64_PATH=./libinjection.so python3 /home/bepi/Desktop/Ph.D_/projects/GPU_stress/code/ScalableGPUMonitoring/cupti/01_pc_sampling_continuous/exe/LeNet5.py > data/raw/PM/lenet_$INJECTION_KERNEL_COUNT.txt
