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
cd 01_pc_sampling_continuous
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
7. Set the LD_LIBRARY_PATH environment variable such that it includes the path to the folder that containes the library that you have just compiled libpc_sampling_continuous.so and run the pl file by specifying the application and the needed settings with the admin permissions. For semplicity a exe.sh file is reported in the folder so you just need to run it with admin permissions. (Take care of the setup that is used to run the application).
```bash
sudo exe.sh
``` 
8. You will receive as output a .dat file which is a generic file format to store data. This will look like a binary file that actually contains a "log line" corresponding to each Performance Counter sample. In order to make it human readable you need copy it into the folder pc_sampling_utility
9. Run the MakeFile
```bash
cd ../pc_sampling_utility
make pc_sampling_utility
``` 
10. An executable file is generated and you need to run it by specifying the path of the .dat file
```bash
./pc_sampling_utility --file-name "<your_dat_file_path>" > log.txt
``` 

11. In this way, the data will be dumped into a log.txt file that you can process in order to parse the gathered statistics.


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

## 2.2  Perfworks metrics monitoring for Compute Capability 7.0
In the past it was possible to query all the metrics avaialable on a specific hardware architecture. Now (for architectures with compute capabilities higher than 7.0) it is deprecated but the following table provides available metrics wirh CC > 7.0

Perfworks metrics starting with sm__ are collected per-SM. Metrics starting with smsp__ are collected per-SM subpartition. However, all corresponding CUPTI metrics are collected per-SM, only.

https://docs.nvidia.com/cupti/main/main.html#id21

If you check the file at the path "cupti/profiling_injection/injection.cpp" I added smsp__inst_executed_pipe_fp64.avg.pct_of_peak_sustained_active metric which basically computes the double_precision_fu_utilization

## 2.3 Instruction to run the profiling on the "simple_target" application
1. Check that the path to the cuda folder is correct
2. Then, use tha MakeFile to compile the target application
```bash
cd profiling_injection
make simple_target
``` 
3. So compile the library that is going to profile the generic application
```bash
make libinjection.so
``` 
4. At this point you can set 2 environment variables:
    - INJECTION_KERNEL_COUNT: Since injection doesn't know how many kernels a target application may run, it must pick a number of kernels to run in a single session, and once this many kernels run, it ends the session and restarts. This sets the number of kernels in a session, defaulting to 10.
    - INJECTION_METRICS: This sets the metrics to gather, separated by space, comma, or semicolon.  Default metrics are:
        - sm__cycles_elapsed.avg
        - smsp__sass_thread_inst_executed_op_dadd_pred_on.avg
        - smsp__sass_thread_inst_executed_op_dfma_pred_on.avg
5. For example, if you need to monitor 20 kernels and you want to monitor the "achieved occupancy" you can run the folling lines
```bash
export INJECTION_KERNEL_COUNT=20
export INJECTION_METRICS="sm__warps_active.avg.pct_of_peak_sustained_active"
``` 
6. Eventually, you can run the following command with the admin permissions and see the results dump in the log.txt file
```bash
sudo env CUDA_INJECTION64_PATH=./libinjection.so ./simple_target > log.txt
``` 

### 2.2 Requirements
Available in CUDA 7.0 and above
admin permissions (sudo is required to run the scripts)



## Checkpoint 1
I think that we should, if possible, mix the profiling metrics that we get for a specific range (to be understood) **2.2** or directly the info gathered from the performance counters (stall reasons) **1.1** that we gather with a specific sampling rate. In alternative we can try to modify "cupti/pc_sampling_continuous/pc_sampling_continuous.cpp" somehow to gather further metrics but I wouldn't have a plan for this. 

## 3 Activity tracing


## 3.1 Asynchronous CUDA API and GPU Activity tracing
The CUPTI Activity API allows you to asynchronously collect a trace of an application’s CPU and GPU CUDA activity. The following terminology is used by the activity API. 

Asynchronous collection of traces refers to the method by which NVIDIA's CUPTI gathers data on an application's CPU and GPU activities without interrupting the application's execution flow. This approach allows developers to analyze performance metrics and behaviors while the application runs normally, minimizing profiling overhead.

In this context, CUPTI utilizes the Activity API to capture detailed information about CUDA operations performed by both the CPU and GPU. It reports these activities through data structures known as activity records, each corresponding to a specific type of activity (e.g., memory copies, kernel executions). These records are then transferred to the developer's analysis tools via activity buffers. CUPTI fills these buffers with activity records as the corresponding activities occur on the CPU and GPU. However, it doesn't guarantee any ordering of the activities in the activity buffer, as activity records for some activity kinds are added lazily (meaning CUPTI defers collecting and adding them to the buffer until a later point in time. This delay can cause activity records to be inserted out of order compared to their actual execution sequence). The CUPTI client is responsible for providing empty activity buffers as necessary to ensure that no records are dropped.

There are different kind of activities that can be traced (the comprehensive list of activities is available in the file cupti/0_common/helper_cupti_activity.h). More than the single activity tracing, enumerators are even more useful because they report ad-hoc reports based on the needed statistics.

https://docs.nvidia.com/cupti/api/group__CUPTI__ACTIVITY__API.html

For example CUpti_ActivityEnvironmentKind reports information about the telemetry
https://docs.nvidia.com/cupti/api/group__CUPTI__ACTIVITY__API.html#_CPPv429CUpti_ActivityEnvironmentKind

And it can be combined with other things to monitor.

## 3.2 Instructions to run the Asynchronous CUDA API and GPU Activity tracing on two simple applications (VectorAdd and VectorSubtraction)
1. Check that the path to the cuda folder is correct
2. Then, use tha MakeFile to compile the cuda script that includes both the CUDA API and GPU Activity tracing and the applications (VectorAdd and VectorSubtraction) 
```bash
cd 03_activity_trace_async
make activity_trace_async
``` 
3. This will produce a binary that you have to execute and dump the output on a log file for eventual postprocessing
```bash
./activity_trace_async > log.txt
``` 
4. Check the produced txt to gather information on the monitored activities.

## 3.3 NVTX Activity tracing
The CUPTI Callback API allows you to register a callback into your own code. Your callback will be invoked when the application being profiled calls a CUDA runtime or driver function, or when certain events occur in the CUDA driver. The following terminology is used by the callback API.

- **Callback Domain**: Callbacks are grouped into domains to make it easier to associate your callback functions with groups of related CUDA functions or events. There are currently four callback domains, as defined by CUpti_CallbackDomain: a domain for CUDA runtime functions, a domain for CUDA driver functions, a domain for CUDA resource tracking, and a domain for CUDA synchronization notification.
- **Callback ID**: Each callback is given a unique ID within the corresponding callback domain so that you can identify it within your callback function. The CUDA driver API IDs are defined in cupti_driver_cbid.h and the CUDA runtime API IDs are defined in cupti_runtime_cbid.h. Both of these headers are included for you when you include cupti.h. The CUDA resource callback IDs are defined by CUpti_CallbackIdResource, and the CUDA synchronization callback IDs are defined by CUpti_CallbackIdSync.
- **Callback Function**: Your callback function must be of type CUpti_CallbackFunc. This function type has two arguments that specify the callback domain and ID so that you know why the callback is occurring. The type also has a cbdata argument that is used to pass data specific to the callback.
- **Subscriber**: A subscriber is used to associate each of your callback functions with one or more CUDA API functions. There can be at most one subscriber initialized with cuptiSubscribe() at any time. Before initializing a new subscriber, the existing subscriber must be finalized with cuptiUnsubscribe().

Each callback domain is described in detail below. Unless explicitly stated, it is not supported to call any CUDA runtime or driver API from within a callback function. Doing so may cause the application to hang.

Using the callback API with the CUPTI_CB_DOMAIN_NVTX domain, you can associate a callback function with NVIDIA Tools Extension (NVTX) API functions. When an NVTX function is invoked in the application, your callback function is invoked as well. For these domains, the cbdata argument to your callback function will be of the type CUpti_NvtxData.

The NVTX library has its own convention for discovering the profiling library that will provide the implementation of the NVTX callbacks. To receive callbacks, you must set the NVTX environment variables appropriately so that when the application calls an NVTX function, your profiling library receives the callbacks.

## 3.4 Instructions to run the NVTX Activity tracing on two simple applications (VectorAdd and VectorSubtraction)
1. Check that the path to the cuda folder is correct
2. Then, use the MakeFile to compile the cuda script that includes both the NVTX activity tracing and the applications (VectorAdd and VectorSubtraction) 
```bash
cd 03_cupti_nvtx
make cupti_nvtx
``` 
3. Set the NVTX_INJECTION64_PATH environment variable such that it includes the path to the library libcupti.so (I think that this is used to have access to the header of available callbacks from cupti). Generally you can find it in the libraries available in your cuda folder
```bash
export NVTX_INJECTION64_PATH="/usr/local/cuda-12/lib64/libcupti.so"
```
4. Run the binary file that does tracing of NVTX callback functions (including cupti callback functions)
```bash
./cupti_nvtx
```

## 3.5 CUPTI (CUDA API and GPU + NVTX) trace Injection
This sample shows how to build an injection library using the CUPTI activity and callback APIs. It can be used to trace CUDA APIs and GPU activities for any CUDA application. **It does not require the CUDA application to be modified.**

## 3.4 Instructions to run the Activity tracing on any application (e.g., VectorAdd)
1. Check that the path to the cuda folder is correct
2. Then, use the MakeFile to compile the cuda script that includes the library for the activity tracing.
```bash
cd 03_cupti_trace_injection
make cupti_trace_injection
cd ..
``` 
3. Move the scripts of your target cuda-based application to the test-apps folder and build it to generate the binaries
```bash
cd test-apps/<app_name>
make 
cd ../..
```
4. Set the CUDA_INJECTION64_PATH environment variable such that it includes the path to the library for the injection. When CUDA_INJECTION64_PATH is set to a shared library, at initialization, CUDA will load the shared object and call the function named 'InitializeInjection'.
   CUDA application needs not to be modified.
```bash
export CUDA_INJECTION64_PATH="./libcupti_trace_injection.so"
```

5. Set the NVTX_INJECTION64_PATH environment variable such that it includes the path to the library for the NVTX tracing to generate NVTX activity records. CUDA application needs not to be modified.
```bash
export NVTX_INJECTION64_PATH="/usr/local/cuda-12/lib64/libcupti.so"
```
6. Run the CUDA application dumping the log to a txt file for further analysis
```bash
./test-apps/<path_to_binary_app> > log.txt
```

## 4.0 CUDA graph trace
CUPTI can collect trace of CUDA Graphs applications without breaking driver performance optimizations. CUPTI has added fields graphId and graphNodeId in the kernel, memcpy and memset activity records to denote the unique ID of the graph and the graph node respectively of the GPU activity. CUPTI issues callbacks for graph operations like graph and graph node creation/destruction/cloning and also for executable graph creation/destruction. The cuda_graphs_trace sample shows how to collect GPU trace and API trace for CUDA Graphs and how to correlate a graph node launch to the node creation API by using CUPTI callbacks for graph operations.

## 4.1 Instruction to run the CUDA graph tracing
1. Check that the path to the cuda folder is correct
2. Then, use the MakeFile to compile the cuda script that includes the library for the activity tracing.
```bash
cd 04_cuda_graphs_trace
make cuda_graphs_trace
``` 
3. This will produce a binary that you have to execute and dump the output on a log file for eventual postprocessing
```bash
./cuda_graphs_trace > log.txt
``` 

## 5.0 Reproducibility of the experiments
Some CUPTI APIs are not guaranteed to return perfectly reproducible results between runs. Numerous factors introduce measurable run-to-run variation in software and hardware performance. There are several suggestions for users who want more reproducible results.

## 5.1 Fixed Clock Rate
Many metrics are directly affected by GPU SM and memory clock frequencies. By default, the GPU keeps clock rates low until work is launched, but clock rates do not boost to full speed immediately, so initial work launched after an idle period may run at low clock speed. Additionally, the target clock rates may vary based on power, thermal, and other factors. Complex interactions between different part of the system mean that these dynamic clock rates may not be reproducible between runs.

To reduce the effect of dynamic clock rates, it is possible to set a fixed clock rate. The GPU will no longer opportunistically boost clock rates above this rate, but it will eliminate the variability after GPU idle and effects of power and thermal variation. Several different methods exist to fix the SM or memory clock rates.

## 5.2 How to exploit nvidia-smi functionalities to fix the clock rate
1. Use the nvidia-smi utility to set the GPU core and memory clocks before attempting measurements. This command is installed by typical driver installations on Windows and Linux. Installation locations may vary by OS version but should be fairly stable.
    - Run commands with sudo to the following commands on Linux-like OSs.
    - To query supported clock rates 
    ```bash
    nvidia-smi --query-supported-clocks=timestamp,gpu_name,gpu_uuid,memory,graphics --format=csv
    ```
    - To set the core and memory clock rates, respectively: 
    ```bash
    nvidia-smi --lock-gpu-clocks=<core_clock_rate>
    nvidia-smi --lock-memory-clocks=<memory_clock_rate>
    ```
    - Perform performance capture or other work.
    - To reset the core and memory clock rates, respectively:
    ```bash
    nvidia-smi --reset-gpu-clocks
    nvidia-smi --reset-memory-clocks
    ```
    - For general use during a project, it may be convenient to write a simple script to lock the clocks, launch your application, and after exit, reset the clocks.
2. Use the DX12 function SetStablePowerState to read the GPU’s predetermined stable power clock rate. The stable GPU clock rate may vary by board. 
    - Modify a DX12 sample to invoke SetStablePowerState.
    - Execute nvidia-smi -q -d CLOCK, and record the Graphics clock frequency with the SetStablePowerState sample running. Use this frequency with the --lock-gpu-clocks option.


## 5.3 Serialization (maybe we don't need to set if we want that the execution of a kernel influences the execution of another)
Work may be submitted to the GPU which can run asynchronously and concurrently. This improves performance by using more of the GPU resources at once, but complicates profiling in two ways - first, kernels running concurrently can impact each other through contention for shared resources. Measurements of these shared resources will include the impact of any concurrently kernels, and it may not be possible to determine the particular impact of any given kernel. Second, by contending for resources with other kernels that are running without precisely guaranteed timing, the timing for a given kernel may be impacted in irreproducible ways.

When CUPTI_ACTIVITY_KIND_CONCURRENT_KERNEL is used to measure kernel timing, kernels are allowed to run concurrently on device. CUPTI_ACTIVITY_KIND_KERNEL may be used instead to measure serialized kernel timing. This will eliminate GPU concurrency within this process, and should provide better run-to-run reproducibility, but the timing may not be as realistic in this mode - kernels will not have to contend for shared resources, which can impact their performance.

## 5.4 Other issues
Beyond variable clock rates and concurrent kernel execution, several other factors can affect application and kernel performance.

The driver normally does not stay loaded when not in use. It takes some time to load and initialize the driver, which may affect performance in noticeable and somewhat irreproducible ways. It is possible to keep the driver persistently loaded which will eliminate this initialization overhead. nvidia-persistenced is one tool to configure this; it can also be configured through nvidia-smi.

## 6.0 Let's try to understand, among all the available tools how many times the application is run
1. **First try (approach)**: Try to see how many times the application kernel is lounched for each of the analysis that we have performed
    - 01_pc_sampling_continuous: I think it adding an overhead but the application is run only ones
    - 02_profiling_injection
    - 03_activity_trace_async
    - 03_cupti_nvtx
    - 03_cupti_trace_injection
    - 04_cuda_graphs_trace

## Checkpoint 2
0. Check the whole current readme.md and change the name of the folders with the prefixes (numbers)
1. Check all the make files and make sure that everything compliles correctly 
2. Complete the afore mentioned list
3. go into the file 01_pc_sampling_continuous and try to trace some of the following events
https://docs.nvidia.com/cupti/api/group__CUPTI__EVENT__API.html
4. Try to do something with the enumerators, if possible. Rather then using the single events
5. Go in the documentation at the following link and try to trace the activity as in **paragraph 3.2**
https://docs.nvidia.com/cupti/api/group__CUPTI__ACTIVITY__API.html#_CPPv429CUpti_ActivityEnvironmentKind
6. Prova a fare tutte queste prove su GPU_burn
### Notes
Each function (activity or kernel) invocation is assigned a unique correlation ID that is identical to the correlation ID in the memcpy, memset, or kernel activity record that is associated with this function. 

**Question**: how many times the application is run to gather metrics? Since some rollup functions are used, the statistics are computed based on multiple runs of the same kernels.

**Question**: how do we choose a correct clock-frequency? Maybe look at **paragraph 5.3, step 2**

**Question**: do we need concurrent execution of the kernels or we need them to be serialized?