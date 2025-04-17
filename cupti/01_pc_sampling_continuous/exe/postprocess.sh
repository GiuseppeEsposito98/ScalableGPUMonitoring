#!/bin/bash

main_directory="exe/bash/postprocessing"
# cd $main_directory

for folder in "$main_directory"/*; do
    if [ -d "$folder" ]; then
        echo "I'm in folder: $PWD"
        
        for file in "$folder"/*; do
            echo $file
            if [ -f "$file" ]; then
                echo "Executing: $file"
                bash $file
            fi
        done
    fi
done