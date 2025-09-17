#!/bin/bash
PERFORMANCE=$1

main_directory="exe/bash/profiling_$PERFORMANCE"
inter='_'
# cd $main_directory
kernels=(1)

for kernel in "${kernels[@]}"; do
    for file in "$main_directory"/*; do
        # if [[ "$file" == *"resnet"* || "$file" == *"lenet"* || "$file" == *"mnasnet"* || "$file" == *"gpuburn5min"* ]]; then
        if ! [[ "$file" == *"gpuburn5min"* ]]; then

            bash $file $kernel 

            echo "End run"
            # sleep 1800

        fi
    done
done