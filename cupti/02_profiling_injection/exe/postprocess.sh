#!/bin/bash
PERFORMANCE=$1
main_directory="exe/bash/postprocessing"
# cd $main_directory

kernels=(3 5 7 15)

for kernel in "${kernels[@]}"; do
    for file in "$main_directory"/*; do
        if [ -f "$file" ]; then
        # if [[ -f "$file" && "$file" == *"gpuburn"* ]]; then
            echo "Processing: $file"
            bash $file $kernel $PERFORMANCE
        fi
    done
done
