SAMPLING_MODE="Parallel"

APP_NAME="backprop"
cp data/raw/$SAMPLING_MODE/1_25_$APP_NAME.dat ../01_pc_sampling_utility/1_25_$APP_NAME.dat
cd ../01_pc_sampling_utility
./pc_sampling_utility --file-name 1_25_$APP_NAME.dat > 1_25_$APP_NAME.txt
python3 parse_data.py --file_name "1_25_$APP_NAME" --sampling_mode "$SAMPLING_MODE"
rm ../01_pc_sampling_utility/1_25_$APP_NAME.dat
rm ../01_pc_sampling_utility/1_25_$APP_NAME.txt

APP_NAME="gaussian"
cd ../01_pc_sampling_continuous
cp data/raw/$SAMPLING_MODE/1_25_$APP_NAME.dat ../01_pc_sampling_utility/1_25_$APP_NAME.dat
cd ../01_pc_sampling_utility
./pc_sampling_utility --file-name 1_25_$APP_NAME.dat > 1_25_$APP_NAME.txt
python3 parse_data.py --file_name "1_25_$APP_NAME" --sampling_mode "$SAMPLING_MODE"
rm ../01_pc_sampling_utility/1_25_$APP_NAME.dat
rm ../01_pc_sampling_utility/1_25_$APP_NAME.txt

APP_NAME="lenet5"
cd ../01_pc_sampling_continuous
cp data/raw/$SAMPLING_MODE/1_25_$APP_NAME.dat ../01_pc_sampling_utility/1_25_$APP_NAME.dat
cd ../01_pc_sampling_utility
./pc_sampling_utility --file-name 1_25_$APP_NAME.dat > 1_25_$APP_NAME.txt
python3 parse_data.py --file_name "1_25_$APP_NAME" --sampling_mode "$SAMPLING_MODE"
rm ../01_pc_sampling_utility/1_25_$APP_NAME.dat
rm ../01_pc_sampling_utility/1_25_$APP_NAME.txt

APP_NAME="sc_gpu"
cd ../01_pc_sampling_continuous
cp data/raw/$SAMPLING_MODE/1_25_$APP_NAME.dat ../01_pc_sampling_utility/1_25_$APP_NAME.dat
cd ../01_pc_sampling_utility
./pc_sampling_utility --file-name 1_25_$APP_NAME.dat > 1_25_$APP_NAME.txt
python3 parse_data.py --file_name "1_25_$APP_NAME" --sampling_mode "$SAMPLING_MODE"
rm ../01_pc_sampling_utility/1_25_$APP_NAME.dat
rm ../01_pc_sampling_utility/1_25_$APP_NAME.txt