import os
import sys
import pandas as pd
from pynvml import *
import argparse
# import ruptures as rpt
import json
import numpy as np
import re
import pynvml

def get_argparser():
    parser = argparse.ArgumentParser(description='Postprocessing for .txt data')
    parser.add_argument('--performance', required=True, help='Either Performance Metrics (PM) or Performance Counters (PC)')
    parser.add_argument('--app', required=True, help='Application name to process')
    return parser

def get_instructionset(nvml_handle):

    
    arch_code = pynvml.nvmlDeviceGetArchitecture(nvml_handle)
    arch_map = {
        0: "Unknown",
        2: "Kepler",
        3: "Maxwell",
        4: "Pascal",
        5: "Volta",
        6: "Turing",
        7: "Ampere",
        8: "Ada Lovelace",
        9: 'Hopper',
        10: 'Blackwell'
    }

    architecture = arch_map.get(arch_code, f"Unknown ({arch_code})")

    if architecture == 'Ada Lovelace':
        # QUESTI VALORI SONO PRESI DA QUI: 
        # https://docs.nvidia.com/cuda/cuda-binary-utilities/index.html#ampere-ampere-instruction-set-table
        # E SONO SPECIFICI PER L'ARCHIRETTURA DELLA GPU (ADA)
        component_map = {
            # Floating-point / FP aritmetica
            "FP": [
                r"FADD", r"FMUL", r"FFMA", r"FMA", r"FSETP", r"FSET",
                r"FADD32I", r"FMUL32I", r"FFMA32I", r"FMA32I",
                r"FSWZADD", r"FSWZADD32I", r"FSESQ", r"FSQRT", r"FRND", r"F2F", r"F2I", r"F2IP", r"F2I.*",
                r"F2IP.*", r"F2F.*"
            ],

            # Interi / operazioni intere
            "INT": [
                r"IADD", r"IMUL", r"IMAD", r"IDP", r"IDP4A", r"IMMA", r"IMNMX", r"ISCADD",
                r"ISETP", r"ISCADD32I", r"IADD32I", r"IMUL32I", r"IMAD32I", r"I2I", r"I2IP", r"I2F",
                r"I2FP.*", r"I2IP.*"
            ],

            # ALU / operazioni logiche, spostamenti, permutazioni, movimenti
            "ALU": [
                r"MOV", r"MOV32I", r"MOVM", r"LOP", r"LOP32I", r"PRMT", r"SEL", r"SGXT",
                r"SHFL", r"SHF", r"LEA", r"LEA\.HI", r"UMOV", r"UIADD3", r"ULDC", 
                r"LOC", r"LOC32I", r"R2P", r"UR2UP", r"UR2UP.*"
            ],

            # SFU / funzioni speciali
            "SFU": [
                r"MUFU", r"RCPSQRT", r"RCP", r"RSQRT", r"SIN", r"COS", r"EX2", r"LG2",
                r"SQRT", r"LOP", r"LOP32I"  # se consideri parti “speciali”
            ],

            # Tensor / MMA / operazioni su tensor cores
            "TENSOR": [
                r"HMMA", r"HMMA\.TF32", r"HMMA32I", r"HMMA_FP16", r"DMMA", r"WMMA", r"MMAS",
                r"MMAD", r"HMNMX2", r"HMUL2", r"HMUL2_32I"
            ]
        }
    elif architecture == 'Ampere':
        component_map = {
            # Floating-point / FP aritmetica (FP32, FP64, varianti)
            "FP": [
                r"FADD", r"FADD32I", r"FMUL", r"FMUL32I", r"FFMA", r"FFMA32I", r"FMA", r"FMA32I",
                r"FSWZADD", r"FSWZADD32I", r"FSESQ", r"FSQRT", r"FRND",
                r"F2F", r"F2IP", r"F2I", r"F2I.*", r"F2IP.*", r"F2F.*"
            ],

            # Interi / operazioni intere (arithmetic integer, multiply, dp, etc.)
            "INT": [
                r"IADD", r"IADD32I", r"IMUL", r"IMUL32I", r"IMAD", r"IMAD32I",
                r"IDP", r"IDP4A", r"IMMA", r"IMNMX", r"ISCADD", r"ISCADD32I",
                r"ISETP", r"I2I", r"I2IP", r"I2F", r"I2FP.*", r"I2IP.*"
            ],

            # ALU / operazioni logiche, spostamenti, permutazioni, movimenti
            "ALU": [
                r"MOV", r"MOV32I", r"MOVM",
                r"LOP", r"LOP32I", r"PRMT", r"SEL", r"SGXT",
                r"SHFL", r"SHF", r"LEA", r"LEA\.HI", r"UMOV", r"UIADD3", r"ULDC",
                r"LOC", r"LOC32I", r"R2P", r"UR2UP", r"UR2UP.*"
            ],

            # SFU / funzioni speciali (trigonometria, reciprocali, etc.)
            "SFU": [
                r"MUFU", r"RCP", r"RSQRT", r"RCPSQRT", r"SIN", r"COS", r"EX2", r"LG2", r"SQRT"
            ],

            # Tensor / MMA / operazioni su tensor cores
            "TENSOR": [
                r"HMMA", r"HMMA\.TF32", r"HMMA32I", r"HMMA_FP16", r"DMMA", r"WMMA",
                r"MMAS", r"MMAD", r"HMNMX2", r"HMUL2", r"HMUL2_32I"
            ]
        }
    return component_map

def main(args):
    
    mapping_table = {
    'gpuburn5min': 'GPU-burn',
    'NN50Perclenet5': 'LeNet5',
    'NN50PercLeNet5': 'LeNet5',
    'NN50Percmnasnet05': 'MnasNet',
    'NN50Percmobilenetv2': 'MobileNetV2',
    'NN50Percresnet18': 'ResNet18',
    'backprop': 'Back Propagation',
    'gaussian': 'Gaussian Elimination',
    'hotspot': 'Hotspot',
    'needle': 'Needleman-Wunsch',
    'scgpu': 'Stream Cluster'
        }

    location_mapping={
        'sm': 'Streaming Multiprocessor',
        'dram': 'Dynamic RAM',
        'l1tex': 'L1 Cache',
        'lts': 'L2 Cache',
        'smsp': 'Streaming Multiprocessor SubPartition'
        }
    
    metric_event_mapping= {
    # Workload
    ## Compute
    'request_cycles_active': 'Number of cycles where the IDC processed requests from SM',
    'instruction_throughput': 'Instruction throughput',
    'inst_executed': 'Executed instructions',
    'inst_issued': 'Issued instructions',
    'sass_thread_inst_executed_op_fp64_pred_on': 'Instructions FP64',
    'sass_thread_inst_executed_op_integer_pred_on': 'Instructions Integers',

    ## Memory
    ### DRAM
    'bytes_read': 'Read Bytes',
    'bytes_write': 'Written bytes',

    ### L1 Cache
    't_sectors_pipe_lsu_mem_global_op_ld_lookup_hit': 'Global Memory Load Sectors – Cache Hit (per Thread Set via LSU)',
    't_sectors_pipe_lsu_mem_global_op_st_lookup_hit': 'Global Memory Store Sectors – Cache Hit (per Thread Set via LSU)',
    't_sectors_pipe_lsu_mem_global_op_red_lookup_hit': 'Global Memory Reduction – Cache Hit (per Thread Set via LSU)',
    't_sectors_pipe_lsu_mem_global_op_atom_lookup_hit': 'Global Memory Atomic – Cache Hit (per Thread Set via LSU)',
    't_sectors_pipe_lsu_mem_global_op_ld': ' Global Memory Load Sectors Served by L1 Cache (via LSU)',
    't_sectors_pipe_lsu_mem_global_op_st': ' Global Memory Store Sectors Served by L1 Cache (via LSU)',
    't_sectors_pipe_lsu_mem_global_op_red': 'Global Memory Reduction Sectors Served by L1 Cache (via LSU)',
    't_sectors_pipe_lsu_mem_global_op_atom': 'Global Memory Atomic Sectors Served by L1 Cache (via LSU)',
    
    ### L2 Cache
    't_sector_op_read_hit_rate': 'L2 hit rate by read instruction',
    't_sector_op_write_hit_rate': 'L2 hit rate by write instruction',

    # Stall
    ## Memory
    'warp_issue_stalled_imc_miss_per_warp_active': 'Warp Issue Stalls Due to IMC (Immediate Constant Cache) Misses per Active Warp ',
    'warp_issue_stalled_long_scoreboard_per_warp_active': 'Warp Issue Stalls Due to Long Scoreboard (Long Wait for Resource) per Active Warp',

    ## Controller
    'warp_issue_stalled_short_scoreboard_per_warp_active': 'Warp Issue Stalls Due to Short Scoreboard (Resource Wait) per Active Warp',
    'warp_issue_stalled_wait_per_warp_active': 'Warp Issue Stalls Due to Wait (Resource/Data Not Ready) per Active Warp',
    'warp_issue_stalled_not_selected_per_warp_active': 'Warp Issue Stalls Due to Not Being Selected per Active Warp',
    'warp_issue_stalled_sleeping_per_warp_active': 'Warp Issue Stalls Due to Sleeping per Active Warp',
    'warp_issue_stalled_membar_per_warp_active': 'Warp Issue Stalls Due to Membar per Active Warp',
    'warp_issue_stalled_barrier_per_warp_active': 'Warp Issue Stalls Due to Barrier per Active Warp',
    'warp_issue_stalled_dispatch_stall_per_warp_active': 'Warp Issue Stalls Due to Dispatch Stall per Active Warp',

    ## Throttle
    'warp_issue_stalled_drain_per_warp_active': 'Warp Issue Stalls Due to Drain (Memory/Resource Write Completion) per Active Warp',
    'warp_issue_stalled_lg_throttle_per_warp_active': 'Warp Issue Stalls Due to Large Unit Throttling (Resource Limitation) per Active Warp',
    'warp_issue_stalled_math_pipe_throttle_per_warp_active': 'Warp Issue Stalls Due to Math Pipe Throttling per Active Warp',
    'warp_issue_stalled_mio_throttle_per_warp_active': 'Warp Issue Stalls Due to MIO Throttling per Active Warp',
    'warp_issue_stalled_tex_throttle_per_warp_active': 'Warp Issue Stalls Due to Texture Throttling per Active Warp',

    ## Others
    'warp_issue_stalled_misc_per_warp_active': 'Warp Issue Stalls Due to Miscellaneous Issues per Active Warp',

    }

    
    data_path = f'data/postprocessed/{args.performance}'

    total_json = {}
    # for app in app_names:
    app = args.app
    if not app in list(mapping_table.keys()):
        mapping_table[app] = app
    total_json[f'{mapping_table[app]}'] = {}
    
    ############################ Performance counters data processing ############################
    pc_file_name = f'{app}_1.csv'
    pc_file_path = os.path.join(data_path, pc_file_name)

    # pc_csv = pd.read_csv(pc_file_path)
    try:
        pc_csv = pd.read_csv(pc_file_path)
    except pd.errors.EmptyDataError:
        print(f"[ERROR] {pc_file_path} is empty or corrupted.")
        sys.exit(1)

    pc_csv['app'] = mapping_table[f'{app}']
    pc_csv['progress'] = (pc_csv['session_id'] - pc_csv['session_id'].min()) / (pc_csv['session_id'].max() - pc_csv['session_id'].min()) * 100
    if app.split('_')[0] == 'hotspot':
        pc_csv['Index'] = range(len(pc_csv))
        pc_csv['progress'] = (pc_csv['Index'] - pc_csv['Index'].min()) / (pc_csv['Index'].max() - pc_csv['Index'].min()) * 100
    pc_csv['Range'] = 1

    pc_csv['HR_location'] = pc_csv['location'].map(location_mapping)

    pc_csv['HR_metric_name'] = pc_csv['metric_name'].map(metric_event_mapping)

    df_l2 = pc_csv[pc_csv['HR_location']=='L2 Cache']
    df_sm = pc_csv[pc_csv['HR_location']=='Streaming Multiprocessor']
    df_smsp = pc_csv[pc_csv['HR_location']=='Streaming Multiprocessor SubPartition']
    df_l1 = pc_csv[pc_csv['HR_location']=='L1 Cache']
    df_dram = pc_csv[pc_csv['HR_location']=='Dynamic RAM']
    
    df_pivot_l2 = df_l2.pivot_table(
        index=["progress", "HR_location", "range_name", "Range", "app", 'rollup_operation', 'Post'],
        columns="HR_metric_name",
        values="metric_value"
    ).reset_index()

    df_pivot_sm = df_sm.pivot_table(
        index=["progress", "HR_location", "range_name", "Range", "app", 'rollup_operation', 'Post'],
        columns="HR_metric_name",
        values="metric_value"
    ).reset_index()

    df_pivot_smsp = df_smsp.pivot_table(
        index=["progress", "HR_location", "range_name", "Range", "app", 'rollup_operation', 'Post'],
        columns="HR_metric_name",
        values="metric_value"
    ).reset_index()

    # print(df_smsp['app'])

    df_pivot_smsp['Memory Stall']=(df_pivot_smsp['Warp Issue Stalls Due to IMC (Immediate Constant Cache) Misses per Active Warp '] +\
                df_pivot_smsp['Warp Issue Stalls Due to Long Scoreboard (Long Wait for Resource) per Active Warp']) /2

    df_pivot_smsp['Controller Stall']=(df_pivot_smsp['Warp Issue Stalls Due to Not Being Selected per Active Warp'] +\
                    df_pivot_smsp['Warp Issue Stalls Due to Short Scoreboard (Resource Wait) per Active Warp'] +\
                    df_pivot_smsp['Warp Issue Stalls Due to Wait (Resource/Data Not Ready) per Active Warp'] +\
                    df_pivot_smsp['Warp Issue Stalls Due to Sleeping per Active Warp'] +\
                    df_pivot_smsp['Warp Issue Stalls Due to Membar per Active Warp'] +\
                    df_pivot_smsp['Warp Issue Stalls Due to Barrier per Active Warp'] ) /7

    df_pivot_smsp['Throttle Stall']=(df_pivot_smsp['Warp Issue Stalls Due to Drain (Memory/Resource Write Completion) per Active Warp'] +\
                                    df_pivot_smsp['Warp Issue Stalls Due to Large Unit Throttling (Resource Limitation) per Active Warp'] +\
                                    df_pivot_smsp['Warp Issue Stalls Due to Math Pipe Throttling per Active Warp'] +\
                                    df_pivot_smsp['Warp Issue Stalls Due to MIO Throttling per Active Warp'] +\
                                    df_pivot_smsp['Warp Issue Stalls Due to Texture Throttling per Active Warp']) /5

    df_pivot_l1 = df_l1.pivot_table(
        index=["progress", "HR_location", "range_name", "Range", "app", 'rollup_operation', 'Post'],
        columns="HR_metric_name",
        values="metric_value"
    ).reset_index()

    df_pivot_l1['Global hit rate'] = (df_pivot_l1['Global Memory Atomic – Cache Hit (per Thread Set via LSU)']+ \
                                    df_pivot_l1['Global Memory Load Sectors – Cache Hit (per Thread Set via LSU)']+\
                                    df_pivot_l1['Global Memory Reduction – Cache Hit (per Thread Set via LSU)']+\
                                    df_pivot_l1['Global Memory Store Sectors – Cache Hit (per Thread Set via LSU)']) / \
                                    (df_pivot_l1[' Global Memory Load Sectors Served by L1 Cache (via LSU)']+ \
                                    df_pivot_l1[' Global Memory Store Sectors Served by L1 Cache (via LSU)']+\
                                    df_pivot_l1['Global Memory Atomic Sectors Served by L1 Cache (via LSU)']+\
                                    df_pivot_l1['Global Memory Reduction Sectors Served by L1 Cache (via LSU)'])

    df_pivot_dram = df_dram.pivot_table(
        index=["progress", "HR_location", "range_name", "Range", "app", 'rollup_operation', 'Post'],
        columns="HR_metric_name",
        values="metric_value"
    ).reset_index()

    pivot_dfs = {
        'L2 Cache': df_pivot_l2, 
        'Streaming Multiprocessor': df_pivot_sm, 
        'Streaming Multiprocessor SubPartition': df_pivot_smsp, 
        'L1 Cache': df_pivot_l1, 
        'Dynamic RAM': df_pivot_dram
        }

    a = pivot_dfs['L1 Cache'].groupby(by=["app"])[['Global hit rate']]\
        .quantile(0.75)\
            .reset_index()
    b = pivot_dfs['L2 Cache'].groupby(by=["app"])[[ 'L2 hit rate by read instruction','L2 hit rate by write instruction']]\
        .quantile(0.75)\
            .reset_index()

    c = pivot_dfs['Streaming Multiprocessor'].groupby(by=["app"])[[ 'Executed instructions','Instruction throughput', 'Issued instructions']]\
        .quantile(0.75)\
            .reset_index()

    d = pivot_dfs['Dynamic RAM'].groupby(by=["app"])[[ 'Read Bytes', 'Written bytes']]\
        .quantile(0.75)\
            .reset_index()

    e = pivot_dfs['Streaming Multiprocessor SubPartition'].groupby(by=["app"])[['Memory Stall', 'Controller Stall', 'Throttle Stall']]\
        .quantile(0.75)\
            .reset_index()

    merge_1 = pd.merge(a, b[['app', 'L2 hit rate by read instruction','L2 hit rate by write instruction']], on='app')
    merge_2 = pd.merge(merge_1, c[['app', 'Executed instructions','Instruction throughput', 'Issued instructions']], on='app')
    merge_3 = pd.merge(merge_2, d[['app','Read Bytes', 'Written bytes']], on='app')
    final_merge = pd.merge(merge_3, e[['app', 'Memory Stall', 'Controller Stall', 'Throttle Stall']], on='app')

    for key in [col for col in final_merge.columns]:
        if key != 'app':
            total_json[f'{mapping_table[app]}'][f'{key}'] = float(final_merge[key])

    #################### Telemetry data processing ###############################
    telemetry_file_name = f'{app}_1_telemetry.csv'
    telemetry_file_path = os.path.join(data_path, telemetry_file_name)
    telemetry_csv = pd.read_csv(telemetry_file_path)

    telemetry_csv['Index'] = range(len(telemetry_csv))
    telemetry_csv['progress'] = telemetry_csv['Index'].transform(
        lambda x: 100 * (x - x.min()) / (x.max() - x.min()) if x.max() > x.min() else 0)
    
    duration = telemetry_csv['Index'].max()

    signal = np.array(telemetry_csv['temperature_C'])
    # algo = rpt.Pelt(model="rbf").fit(signal)
    # result = algo.predict(pen=51)
    # response_time = result[0]

    steady_temp = telemetry_csv[telemetry_csv['Index']>125]['temperature_C'].mean()

    max_temp = telemetry_csv['max_temp'].mean()

    telemetry_csv['total_energy_J'] = telemetry_csv['total_energy_mJ']/1000
    spent_energy = telemetry_csv[['total_energy_J']].max() - telemetry_csv[['total_energy_J']].min()
    spent_energy['mean_energy_J'] = spent_energy['total_energy_J']/(duration/60)
    delta_cf = telemetry_csv['clock_max_sm'] - telemetry_csv['clock_sm_MHz']
    current_cf = telemetry_csv['clock_sm_MHz'].mean()
    max_cf = telemetry_csv['clock_max_sm'].mean()
    
    total_json[f'{mapping_table[app]}']['Steady Temp °C'] = steady_temp
    total_json[f'{mapping_table[app]}']['Max Temp °C'] = max_temp
    total_json[f'{mapping_table[app]}']['Energy spent J/min'] = spent_energy['mean_energy_J']
    total_json[f'{mapping_table[app]}']['Delta Clock Frequency MHz'] = delta_cf.mean()
    total_json[f'{mapping_table[app]}']['Clock Frequency MHz'] = current_cf
    total_json[f'{mapping_table[app]}']['Max Clock Frequency MHz'] = max_cf



    # total_json[f'{mapping_table[app]}']['response (s)'] = response_time,
    
    #################### POWER ESTIMATION ####################

    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)

    component_map = get_instructionset(handle)

    idle_power_mw, _ = pynvml.nvmlDeviceGetPowerManagementLimitConstraints(handle)
    idle_power = idle_power_mw/1000

    # path = '/home/bepi/Desktop/Ph.D_/projects/GPU_stress/code/ScalableGPUMonitoring/NCU/data/raw/ncu/gpuburnsass_1.csv'
    raw_file_data_path = f'data/raw/{args.performance}/{app}sass_1.csv'

    max_power = {
        "FP": 0.2,
        "INT": 0.25,
        "ALU": 0.2,
        "SFU": 0.5,
        "TENSOR": 0.2,
        "Const_SM": 0.813,
    }

    df = pd.read_csv(f"{raw_file_data_path}", header=None, names=["Address", "Instruction"])

    df["Instruction"] = df["Instruction"].str.strip()

    df["Opcode"] = df["Instruction"].str.split().str[0]

    opcode_counts = df["Opcode"].value_counts().reset_index()

    # print(opcode_counts)
    opcode_counts = opcode_counts[~opcode_counts["Opcode"].str.lower().isin(["source", "compare", "ampere_sgemm_64x64_nn"])]

    counts = {k: 0 for k in max_power}
    count = 0
    print(counts.keys())
    for _, row in opcode_counts.iterrows():
        opcode = row["Opcode"]
        count = row["count"]
        for comp, patterns in component_map.items():
            if any(re.match(p, opcode) for p in patterns):
                count += 1
                counts[comp] += count
                break
        
    total_insts = opcode_counts["count"].sum()
    access_rates = {k: v / total_insts for k, v in counts.items()}
    print(access_rates)

    spec_linear_components = [
    "FP", "REG", "INT", "FDS", "Texture_Cache",
    "Const_Cache", "GlobalMem", "LocalMem"
    ]

    def piecewise_linear(rate):
        if rate <= 0:
            return 0
        return 0.1365 * np.log(rate) + 1.001375

    # Applica la conversione solo ai componenti Spec.Linear
    adj_access_rates = {}
    for k, v in access_rates.items():
        if k in spec_linear_components:
            adj_access_rates[k] = piecewise_linear(v)
        else:
            adj_access_rates[k] = v

    runtime_power_base = sum(max_power[k] * access_rates[k] for k in max_power)

    # runtime_power_base = sum(max_power[k] * access_rates[k] for k in max_power)

    Num_SMs = 24
    alpha = (10 - 1.1) / Num_SMs
    beta = 1.1

    active_sms = np.arange(1, Num_SMs + 1)
    # ATTENZIONE: QUESTO MODELLO ASSUME CHE LA POTENZA SIA IMPIEGATA SOLO DA SM CHE SONO COMPLETAMENTE ATTIVI: QUESTO DETERMINA A DIFFERENZA W.R.T LA POWER REALE
    # IL POWER GATING È IL FENOMENO CHE GENERA QUESTO DELTA W.R.T. LA POWER REALE
    runtime_power = runtime_power_base * np.log10(alpha * active_sms + beta)

    tot_power = idle_power + (runtime_power[-1]*Num_SMs)

    total_json[f'{mapping_table[app]}']['Power_est'] = tot_power

    with open(f"{data_path}/{app}_evaluation.json", "w", encoding="utf-8") as f:
        json.dump(total_json, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    argparser = get_argparser()
    main(argparser.parse_args())