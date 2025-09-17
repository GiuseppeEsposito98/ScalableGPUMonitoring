import csv
import time
import os
import threading
from datetime import datetime
from pynvml import *
import argparse
from pynvml import (
    NVML_MEMORY_ERROR_TYPE_CORRECTED,
    NVML_MEMORY_ERROR_TYPE_UNCORRECTED,
    NVML_VOLATILE_ECC,
    NVML_AGGREGATE_ECC
)

sampling_ns = 1_000_000_000  # 1 secondo

def sample_telemetry(device, index):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    name = nvmlDeviceGetName(device)
    temp = nvmlDeviceGetTemperature(device, NVML_TEMPERATURE_GPU)
    util = nvmlDeviceGetUtilizationRates(device)
    mem = nvmlDeviceGetMemoryInfo(device)
    clock_sm = nvmlDeviceGetClockInfo(device, NVML_CLOCK_SM)
    clock_mem = nvmlDeviceGetClockInfo(device, NVML_CLOCK_MEM)
    clock_gr = nvmlDeviceGetClockInfo(device, NVML_CLOCK_GRAPHICS)

    try:
        fan = nvmlDeviceGetFanSpeed(device)
    except NVMLError:
        fan = -1

    try:
        power = nvmlDeviceGetPowerUsage(device) / 1000.0
    except NVMLError:
        power = -1

    try:
        ecc_vol_corr = nvmlDeviceGetTotalEccErrors(device, NVML_MEMORY_ERROR_TYPE_CORRECTED, NVML_VOLATILE_ECC)
    except NVMLError:
        ecc_vol_corr = -1

    try:
        ecc_vol_uncorr = nvmlDeviceGetTotalEccErrors(device, NVML_MEMORY_ERROR_TYPE_UNCORRECTED, NVML_VOLATILE_ECC)
    except NVMLError:
        ecc_vol_uncorr = -1

    try:
        ecc_agg_corr = nvmlDeviceGetTotalEccErrors(device, NVML_MEMORY_ERROR_TYPE_CORRECTED, NVML_AGGREGATE_ECC)
    except NVMLError:
        ecc_agg_corr = -1

    try:
        ecc_agg_uncorr = nvmlDeviceGetTotalEccErrors(device, NVML_MEMORY_ERROR_TYPE_UNCORRECTED, NVML_AGGREGATE_ECC)
    except NVMLError:
        ecc_agg_uncorr = -1

    return [
        timestamp,
        index,
        name,
        temp,
        util.gpu,
        util.memory,
        mem.total // (1024 * 1024),
        mem.used // (1024 * 1024),
        mem.free // (1024 * 1024),
        clock_sm,
        clock_mem,
        clock_gr,
        fan,
        power,
        ecc_vol_corr,
        ecc_vol_uncorr,
        ecc_agg_corr,
        ecc_agg_uncorr
    ]

def write_row(csv_file, device, index):
    try:
        with open(csv_file, mode='a', newline='') as f:
            writer = csv.writer(f)
            while True:
                row = sample_telemetry(device, index)
                writer.writerow(row)
                f.flush()
                time.sleep(sampling_ns / 1e9)
    except KeyboardInterrupt:
        print(f"[GPU {index}] Interrotto.")
    except Exception as e:
        print(f"[GPU {index}] Errore: {e}")

def get_argparser():
    parser = argparse.ArgumentParser(description='Telemetry monitor for multiple GPUs')
    parser.add_argument('--file_name', required=True, help='Base file name for CSV')
    parser.add_argument('--performance', required=True, help='Performance type (e.g. PM or PC)')
    return parser

def main(args):
    nvmlInit()
    device_count = nvmlDeviceGetCount()


    os.makedirs(f"data/postprocessed/{args.performance}", exist_ok=True)

    header = [
        "timestamp", "gpu_index", "name", "temperature_C",
        "util_gpu_percent", "util_mem_percent",
        "mem_total_MB", "mem_used_MB", "mem_free_MB",
        "clock_sm_MHz", "clock_mem_MHz", "clock_graphics_MHz",
        "fan_speed_percent", "power_draw_W",
        "ecc_volatile_corrected", "ecc_volatile_uncorrected",
        "ecc_aggregate_corrected", "ecc_aggregate_uncorrected"
    ]

    threads = []

    for index in range(device_count):
        device = nvmlDeviceGetHandleByIndex(index)
        csv_file = f"data/postprocessed/{args.performance}/{args.file_name}{index}_telemetry.csv"

        # Scrivi header CSV
        with open(csv_file, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)

        # Thread separato per ogni GPU
        t = threading.Thread(target=write_row, args=(csv_file, device, index), daemon=True)
        threads.append(t)
        t.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrotto dall'utente.")
    finally:
        nvmlShutdown()

if __name__ == '__main__':
    argparser = get_argparser()
    main(argparser.parse_args())
