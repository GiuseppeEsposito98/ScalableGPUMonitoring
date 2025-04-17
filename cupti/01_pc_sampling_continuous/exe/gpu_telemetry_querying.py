import csv
import time
from pynvml import *

# Inizializza NVML
nvmlInit()
device = nvmlDeviceGetHandleByIndex(0)  # GPU 0

# Nome file
csv_file = "gpu_telemetry.csv"

# Header CSV
header = [
    "timestamp_ns", "gpu_index", "name", "temperature_C",
    "util_gpu_percent", "util_mem_percent",
    "mem_total_MB", "mem_used_MB", "mem_free_MB",
    "clock_sm_MHz", "clock_mem_MHz", "clock_graphics_MHz",
    "fan_speed_percent", "power_draw_W"
]

# Sampling period (in nanosecondi)
sampling_ns = 500_000  # 500_000 ns = 0.5 ms

# Funzione per leggere una riga di dati
def sample_telemetry():
    timestamp = time.perf_counter_ns()
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
        fan = -1  # oppure 'N/A' se preferisci un valore testuale
    
    try:
        power = nvmlDeviceGetPowerUsage(device) / 1000.0  # in W
    except NVMLError:
        power = -1  # oppure 'N/A'

    return [
        timestamp,
        0,
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
        power
    ]

# Scrivi header
with open(csv_file, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)

# Loop di logging
try:
    with open(csv_file, mode='a', newline='') as f:
        writer = csv.writer(f)
        while True:
            row = sample_telemetry()
            writer.writerow(row)
            f.flush()  # salva subito
            time.sleep(sampling_ns / 1e9)  # converti ns → sec
except KeyboardInterrupt:
    print("Interrotto dall'utente.")
finally:
    nvmlShutdown()