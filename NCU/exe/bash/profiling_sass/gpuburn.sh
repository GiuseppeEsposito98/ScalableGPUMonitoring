
ncu --csv --log-file data/raw/ncu/gpuburnsass_1.csv --force-overwrite \
    --print-source sass --page source --force-overwrite \
    --target-processes all --replay-mode kernel --kernel-name-base function --launch-skip-before-match 0 \
    --profile-from-start 1 --cache-control all --clock-control base --apply-rules yes    --import-source no \
    --check-exit-code yes \
    test-apps/gpu-burn/gpu_burn -m 50%    -c test-apps/gpu-burn/compare.ptx 300
