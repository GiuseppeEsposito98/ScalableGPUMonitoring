
ncu --csv --force-overwrite --log-file data/raw/ncu/hotspotsass_1.csv\
    --print-source sass --page source --force-overwrite \
    --target-processes all --replay-mode kernel --kernel-name-base function --launch-skip-before-match 0 \
    --profile-from-start 1 --cache-control all --clock-control base --apply-rules yes    --import-source no \
    --check-exit-code yes \
    ./test-apps/gpu-rodinia/bin/linux/cuda/hotspot 1024 5 5 ./test-apps/gpu-rodinia/hotspot/temp_1024 ./test-apps/gpu-rodinia/hotspot/power_1024 log.log