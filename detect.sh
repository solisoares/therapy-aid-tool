# Detect any input source with a Neural Network (NN) in nn folder

# --- EDIT ---
# NN name (project name, local only)
nn_name=3objs

# Detect name (run name)
detect_name=exp

# Data Path
data=/home/alexandre/asd-research/nn/$nn_name/$nn_name.yaml

# Weights Path
weights=/home/alexandre/asd-research/nn/$nn_name/runs/train/$train_name/weights/best.pt

# Hyperparameters
imgsz=256


# --- DO NOT EDIT --- 
# YOLOv5 detect file
detect=~/yolov5/detect.py

# Project(NN) Path (local only)
project=/home/alexandre/asd-research/nn/$nn_name

# Run name
run=runs/test/$detect_name


# --- EDIT if necessary ---
# Detect It!
python $detect --data $data --weights $weights --imgsz $imgsz --source $source --project $project --name $run # --conf-th 0.5 --iou-th 0.5