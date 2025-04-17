#!/bin/bash

main_directory="exe/bash/postprocessing"
# cd $main_directory

kernels=(1 2 3 4 5)

for kernel in "${kernels[@]}"; do
    for file in "$main_directory"/*; do
        if [ -f "$file" ]; then
            echo "Executing: $file"
            bash $file $kernel
        fi
    done
done
