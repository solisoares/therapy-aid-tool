# Detect any input source with a Neural Network (NN) in nn folder
repo=/home/alexandre/therapy-aid-tool

# ------------------------------ EDIT ------------------------------
# NN name (project name, local only)
nn_name=3objs

# Train run
train_run=full1

# Detection run
detection_run=confth-075_pass-to-parser

# Data Path
data=$repo/nn/$nn_name/$nn_name.yaml

Weights Path
weights=$repo/nn/$nn_name/runs/train/$train_run/weights/best.pt

# Parameters
imgsz=256

# Source
source=$repo/sample_data/test_video.avi


# --------------------------- DO NOT EDIT --------------------------- 
# YOLOv5 detect file
detect=~/yolov5/detect.py

# Project(NN) Path (local only)
project=$repo/nn/$nn_name

# Run path (relative to project)
run=runs/test/$train_run/$detection_run


# ------------------------ EDIT if necessary ------------------------ 
# Detect It!
python $detect --data $data --weights $weights --imgsz $imgsz --source $source --project $project --name $run --save-txt --save-conf --conf-th 0.75 # --iou-th 0.5