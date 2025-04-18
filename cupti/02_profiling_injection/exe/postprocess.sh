#!/bin/bash
PERFORMANCE=$1
main_directory="exe/bash/postprocessing"
# cd $main_directory

kernels=(1 10 20 30 50 80 100)

for kernel in "${kernels[@]}"; do
    for file in "$main_directory"/*; do
        if [ -f "$file" ]; then
            echo "Executing: $file"
            bash $file $kernel $PERFORMANCE
        fi
    done
done
