# Workload
## Compute
INJECTION_METRICS="sm__inst_executed.avg.per_cycle_elapsed," # Executed Ipc Elapsed
INJECTION_METRICS=$INJECTION_METRICS"sm__instruction_throughput.avg.pct_of_peak_sustained_active," # SM Busy
INJECTION_METRICS=$INJECTION_METRICS"sm__inst_executed.avg.per_cycle_active," # Executed Ipc Active
INJECTION_METRICS=$INJECTION_METRICS"sm__inst_issued.avg.pct_of_peak_sustained_active," # Issue Slots Busy
INJECTION_METRICS=$INJECTION_METRICS"sm__inst_issued.avg.per_cycle_active," # Issued Ipc Active
INJECTION_METRICS=$INJECTION_METRICS"smsp__sass_thread_inst_executed_op_fp64_pred_on.sum,"  # inst_fp_64
INJECTION_METRICS=$INJECTION_METRICS"smsp__sass_thread_inst_executed_op_integer_pred_on.sum," # inst_integer

## Memory 
INJECTION_METRICS=$INJECTION_METRICS"dram__bytes_read.sum.per_second," # dram_read_throughput
INJECTION_METRICS=$INJECTION_METRICS"dram__bytes_write.sum.per_second," # dram_write_throughput

INJECTION_METRICS=$INJECTION_METRICS"l1tex__t_sectors_pipe_lsu_mem_global_op_ld_lookup_hit.sum," # global_hit_rate
INJECTION_METRICS=$INJECTION_METRICS"l1tex__t_sectors_pipe_lsu_mem_global_op_st_lookup_hit.sum," # global_hit_rate
INJECTION_METRICS=$INJECTION_METRICS"l1tex__t_sectors_pipe_lsu_mem_global_op_red_lookup_hit.sum," # global_hit_rate
INJECTION_METRICS=$INJECTION_METRICS"l1tex__t_sectors_pipe_lsu_mem_global_op_atom_lookup_hit.sum," # global_hit_rate
INJECTION_METRICS=$INJECTION_METRICS"l1tex__t_sectors_pipe_lsu_mem_global_op_ld.sum," # global_hit_rate
INJECTION_METRICS=$INJECTION_METRICS"l1tex__t_sectors_pipe_lsu_mem_global_op_st.sum," # global_hit_rate
INJECTION_METRICS=$INJECTION_METRICS"l1tex__t_sectors_pipe_lsu_mem_global_op_red.sum," # global_hit_rate
INJECTION_METRICS=$INJECTION_METRICS"l1tex__t_sectors_pipe_lsu_mem_global_op_atom.sum," # global_hit_rate

INJECTION_METRICS=$INJECTION_METRICS"lts__t_sector_op_read_hit_rate.pct," # L2 hit rate read
INJECTION_METRICS=$INJECTION_METRICS"lts__t_sector_op_write_hit_rate.pct," # L2 hit rate write

# Stall
## Memory
INJECTION_METRICS=$INJECTION_METRICS"smsp__warp_issue_stalled_imc_miss_per_warp_active.pct," # stall_constant_memory_dependency
INJECTION_METRICS=$INJECTION_METRICS"smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct," # stall_memory_dependency

## Controller
INJECTION_METRICS=$INJECTION_METRICS"smsp__warp_issue_stalled_wait_per_warp_active.pct," # stall_exec_dependency
INJECTION_METRICS=$INJECTION_METRICS"smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct," # stall_exec_dependency
INJECTION_METRICS=$INJECTION_METRICS"smsp__warp_issue_stalled_not_selected_per_warp_active.pct," # stall_not_selected
INJECTION_METRICS=$INJECTION_METRICS"smsp__warp_issue_stalled_sleeping_per_warp_active.pct," # stall_sleeping
INJECTION_METRICS=$INJECTION_METRICS"smsp__warp_issue_stalled_barrier_per_warp_active.pct," # stall_sync
INJECTION_METRICS=$INJECTION_METRICS"smsp__warp_issue_stalled_membar_per_warp_active.pct," # stall_sync

# Throttle
INJECTION_METRICS=$INJECTION_METRICS"smsp__warp_issue_stalled_tex_throttle_per_warp_active.pct," # stall_texture
INJECTION_METRICS=$INJECTION_METRICS"smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct," # stall_pipe_busy
INJECTION_METRICS=$INJECTION_METRICS"smsp__warp_issue_stalled_math_pipe_throttle_per_warp_active.pct," # stall_pipe_busy
INJECTION_METRICS=$INJECTION_METRICS"smsp__warp_issue_stalled_lg_throttle_per_warp_active.pct," # stall_memory_throttle
INJECTION_METRICS=$INJECTION_METRICS"smsp__warp_issue_stalled_drain_per_warp_active.pct" # stall_memory_throttle


ncu --csv --force-overwrite --log-file data/raw/ncu/NN50PercLeNet5_1.csv \
        --target-processes all --replay-mode kernel --kernel-name-base function --launch-skip-before-match 0 \
        --metrics ${INJECTION_METRICS} \
        --profile-from-start 1 --cache-control all --clock-control base --apply-rules yes \
        --import-source no --check-exit-code yes     \
        python3 /home/g.esposito/ScalableGPUMonitoring/NCU/test-apps/NNs/evaluate.py\
                --model_name LeNet5 \
                --dataset_name MNIST \
                --batch_size 10000 \
                --num_iterations 10000000000000000000 \
                --duration 300
