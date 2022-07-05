# Validate with a Trained NN

# ------------------------------ EDIT ------------------------------
# NN name (project name, local only)
nn_name=3objs

# Train run
train_run=TRAIN_EXAMPLE

# Validation run
val_run=VALIDATION_EXAMPLE

# Data Path
data=/home/alexandre/therapy-aid-tool/nn/3objs/3objs.yaml

# Weights Path
weights=/home/alexandre/therapy-aid-tool/nn/3objs/runs/full1/train/weights/best.pt

# Parameters
imgsz=256
batch=1

# --------------------------- DO NOT EDIT --------------------------- 
repo=/home/alexandre/therapy-aid-tool

# YOLOv5 val file
val=~/yolov5/val.py

# Project(NN) Path (local only)
project=$repo/nn/$nn_name

# Run path (relative to project)
run=runs/$train_run/val/$val_run

# -------------------------- Validate It! -------------------------- 
python $val --data $data --weights $weights --imgsz $imgsz --batch $batch --project $project --name $run