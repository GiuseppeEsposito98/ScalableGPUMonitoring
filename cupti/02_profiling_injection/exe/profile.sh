#!/bin/bash

main_directory="exe/bash/profiling"
inter='_'
# cd $main_directory

export PATH="/home/bepi/anaconda3/bin:$PATH"
source /home/bepi/anaconda3/bin/activate
conda deactivate 

conda activate gpustress

kernels=(1 2 3 4 5)

for kernel in "${kernels[@]}"; do
    for file in "$main_directory"/*; do
        if [ -f "$file" ]; then

            echo "Executing telemetry controller in parallel"
            echo $file

            IFS='/' read -ra parts <<< "$file"

            IFS='.' read -ra parts1 <<< "${parts[3]}"

            python3 exe/gpu_telemetry_querying.py --file_name ${parts1[0]}$inter$kernel &
            PID_CONTROLLER=$!

            echo "Executing: $file"
            bash $file $kernel 

            kill "$PID_CONTROLLER"

            wait "$PID_CONTROLLER" 2>/dev/null

            echo "End run"

        fi
    done
done