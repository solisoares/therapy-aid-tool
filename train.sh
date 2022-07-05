# Train a NN

# ------------------------------ EDIT ------------------------------
# NN name (project name, local and wandb)
nn_name=3objs

# Train run
train_run=TRAIN_EXAMPLE

# Data Path
data=/home/alexandre/therapy-aid-tool/nn/3objs/3objs.yaml

# Weights Path
weights=/home/alexandre/therapy-aid-tool/nn/3objs/runs/full1/train/weights/best.pt

# Parameters
imgsz=256
batch=1
epochs=1

# --------------------------- DO NOT EDIT --------------------------- 
repo=/home/alexandre/therapy-aid-tool

# YOLOv5 train file
train=~/yolov5/train.py

# Project(NN) path (local and wandb)
project=$repo/nn/$nn_name

# Run relative path (relative to project)
run=runs/$train_run/train

# ---------------------------- Train It! ---------------------------- 
python3 $train  --data $data --weights $weights --imgsz $imgsz --batch $batch --epochs $epochs --project $project --name $run