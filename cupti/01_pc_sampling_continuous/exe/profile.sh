#!/bin/bash

main_directory="exe/bash/profiling"
# cd $main_directory

for folder in "$main_directory"/*; do
    if [ -d "$folder" ]; then
        echo "I'm in folder: $folder"
        
        for file in "$folder"/*; do
            echo $file
            if [ -f "$file" ] && [[ "$file" == *Serialized* ]]; then
                echo "Executing: $file"
                sudo bash $file
            fi
        done
    fi
done