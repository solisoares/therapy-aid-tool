# Detect with a Trained NN

# ------------------------------ EDIT ------------------------------
# NN name (project name, local only)
nn_name=3objs

# Train run
train_run=TRAIN_EXAMPLE

# Detection run
detection_run=DETECTION_EXAMPLE

# Data Path
data=/home/alexandre/therapy-aid-tool/nn/3objs/3objs.yaml

# Weights Path
weights=/home/alexandre/therapy-aid-tool/nn/3objs/runs/full1/train/weights/best.pt

# Parameters
imgsz=256

# Source
source=/home/alexandre/therapy-aid-tool/sample_data/test_video.avi

# --------------------------- DO NOT EDIT --------------------------- 
repo=/home/alexandre/therapy-aid-tool

# YOLOv5 detect file
detect=~/yolov5/detect.py

# Project(NN) Path (local only)
project=$repo/nn/$nn_name

# Run path (relative to project)
run=runs/$train_run/test/$detection_run

# --------------------------- Detect It! --------------------------- 
python $detect --data $data --weights $weights --imgsz $imgsz --source $source --project $project --name $run --save-txt --save-conf --conf-th 0.75 # --iou-th 0.5