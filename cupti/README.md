## 1.0 CUPTI Continuous Program Counter Sampling API
The sampler in each streaming multiprocessor (SM) selects an active warp and records both its program counter and the warp scheduler state. The sampler selects a random active warp, while the scheduler may select a different warp to issue in the same cycle. The collected metrics can be correlated with the executed instructions, but they lack time resolution.

Features:
- Two sampling modes – Continuous (concurrent kernels) or Serialized (one kernel at a time)​.
- Option to collect specific stall reasons.​
- Cupti_pcsampling_utils has APIs for correlating GPU assembly to CUDA-C source code and for reading and writing the PC sampling data to files. 


|  Configuration Attribute  |                                                                                                                                             Description                                                                                                                                            |                                Default Value                                |                                                              Comparison of PC Sampling APIs with  CUPTI PC Sampling Activity APIs                                                              |                                                                                                           Guideline to Tune Configuration Option                                                                                                          |
|:-------------------------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:---------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|      Collection mode      |                                                                                                                   PC Sampling collection mode -  Continuous or Kernel Serialized                                                                                                                   |                                  Continuous                                 |                        Continuous mode is new.   Kernel Serialized mode is equivalent to the kernel level functionality provided by the CUPTI PC sampling Activity APIs.                       |                                                                                                                                                                                                                                                           |
|      Sampling period      |                            Sampling period for PC Sampling. Valid values for the sampling periods  are between 5 to 31 both inclusive. This will set the sampling period to  (2^samplingPeriod) cycles. e.g. for sampling period = 5 to 31, cycles = 32, 64, 128,…, 2^31                           |                CUPTI defined value is based on number of SMs                | Dropped current support for 5 levels(MIN, LOW, MID, HIGH, MAX) for sampling period.  The new “sampling period” is equivalent to the “samplingPeriod2” field in CUpti_ActivityPCSamplingConfig. |                                    Low sampling period means a high sampling frequency which can result in  dropping of samples. Very high sampling period can cause low sampling  frequency and no sample generation.                                    |
|        Stall reason       |                                                                                                   Stall reasons to collect Input is a pointer to an array of the stall reason indexes to collect.                                                                                                  |                     All stall reasons will be collected                     |                  With the CUPTI PC sampling Activity APIs there is no option to select  which stall reasons to collect. Also the list of supported stall reasons has changed.                  |                                                                                                                                                                                                                                                           |
|    Scratch buffer size    | Size of SW buffer for raw PC counter data downloaded from HW buffer.  Approximately it takes 16 Bytes (and some fixed size memory) to accommodate one PC with one stall reason  e.g. 1 PC with 1 stall reason = 32 Bytes  1 PC with 2 stall reason = 48 Bytes  1 PC with 4 stall reason = 96 Bytes | 1 MB  (which can accommodate approximately 5500 PCs with all stall reasons) |                                                                                                                                                                                                |                         Clients can choose scratch buffer size as per memory budget.  Very  small scratch buffer size can cause runtime overhead as more iterations   would be required to accommodate and process more PC samples                        |
|    Hardware buffer size   |                                                                                                Size of HW buffer in bytes.  If sampling period is too less, HW buffer can overflow and drop PC data                                                                                                |                                    512 MB                                   |                                                                                                                                                                                                | Device accessible buffer for samples. Less hardware buffer size with low  sampling periods, can cause overflow and dropping of PC data. High  hardware buffer size can impact application execution due to lower  amount of device memory being available |
| Enable start/stop control |                                                                                              Control over PC Sampling data collection range.  1 - Allows user to start and stop PC Sampling using APIs                                                                                             |                                 0 (disabled)                                |                                                                                                                                                                                                |                                                                                                                                                                                                                                                           |

Check the link for the Stall reasons Mapping table from PC Sampling Activity APIs to PC Sampling APIs:

https://docs.nvidia.com/cupti/main/main.html#stall-reasons-mapping-table


###  1.1 Instructions to run
1. Check that the path to the cuda folder is correct
2. Then, use tha MakeFile to compile the library that is going to sample the Performance Counters
```bash
cd pc_sampling_continuous
make pc_sampling_continuous
``` 
3. A libpc_sampling_continuous.pl is provided to help you in configuring the Performance Counter sampling.
```bash
# Check the available modes
./libpc_sampling_continuous.pl --help
``` 
4. As you can see, the tool requires an application to lunch in thread that is parallel to the sampling
5. In the folder test-apps, a simple application (VectorAdd) is provided. You can add as many application as you need to be monitored
6. Generate the executable for your own application. 
7. Set the LD_LIBRARY_PATH environment variable such that it includes the path to the folder that containes the library that you have just compiled libpc_sampling_continuous.so
```bash

sudo export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:"<folder_to_pc_sampling_continuous.so>"
``` 
8. Run the pl file by specifying the application and the needed settings with the admin permissions. 
```bash
# Check the available modes
sudo ./libpc_sampling_continuous.pl --app "test-apps/<your_app_path>"
``` 
9. You will receive as output a .dat file which is a generic file format to store data. This will look like a binary file that actually contains a "log line" corresponding to each Performance Counter sample. In order to make it human readable you need copy it into the folder pc_sampling_utility
10. Run the MakeFile
```bash
cd ../pc_sampling_utility
make pc_sampling_utility
``` 
11. An executable file is generated and you need to run it by specifying the path of the .dat file
```bash
./pc_sampling_utility --file-name "<your_dat_file_path>" > log.txt
``` 

12. In this way, the data will be dumped into a log.txt file that you can process in order to parse the gathered statistics.


## 2.0 Profiling injection
A metric is a quantifiable measurement used to assess the performance and efficiency of a CUDA kernel. Metrics can provide insights into various computational characteristics such as execution time, instruction throughput, or cache efficiency.

When profiling a kernel, metrics are predefined to capture particular performance data. After the profiling is complete, the values associated with these metrics allow developers to analyze the kernel’s behavior, identify performance bottlenecks, and make informed optimizations.

For example, common metrics during kernel profiling might include:
- **Execution Time**: The duration the kernel takes to complete.
- **Memory Bandwidth**: The amount of data transferred between units.
- **Instruction Throughput**: The number of instructions executed per second.
- **Cache Hit Rate**: The percentage of memory accesses that are served by the cache.

(It is slightly complicated to select metrics. However, the documentation suggests the following metrics to be )

PM sampling supports the collection of a wide variety of metrics. The table below lists some useful metrics that provide insights into the utilization of different units in the GPU.

https://docs.nvidia.com/cupti/main/main.html#metrics-table

## 2.1 Enumeration
Enumeration paragraph gives you an idea on how you can apply rollups and which submetrics you can gather out of the above-mentioned metrics.

https://docs.nvidia.com/cupti/main/main.html#enumeration

## 2.2
In the past it was possible to query all the metrics avaialable on a specific hardware architecture. Now (for architectures with compute capabilities higher than 7.0) it is deprecated but the following table provides available metrics wirh CC > 7.0

Perfworks metrics starting with sm__ are collected per-SM. Metrics starting with smsp__ are collected per-SM subpartition. However, all corresponding CUPTI metrics are collected per-SM, only.

https://docs.nvidia.com/cupti/main/main.html#id21

If you check the file at the path "cupti/profiling_injection/injection.cpp" I added smsp__inst_executed_pipe_fp64.avg.pct_of_peak_sustained_active metric which basically computes the double_precision_fu_utilization

### 2.2 Requirements
Available in CUDA 7.0 and above

# CONCLUSION
I think that we should, if possible, mix the profiling metrics that we get for a specific range (to be understood) **2.2** or directly the info gathered from the performance counters (stall reasons) **1.1** that we gather with a specific sampling rate. In alternative we can try to modify "cupti/pc_sampling_continuous/pc_sampling_continuous.cpp" somehow to gather further metrics but I wouldn't have a plan for this. 