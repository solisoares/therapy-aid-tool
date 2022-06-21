# Train any Neural Network (NN) available in nn folder
repo=/home/alexandre/therapy-aid-tool

# ------------------------------ EDIT ------------------------------
# NN name (project name, local and wandb)
nn_name=3objs

# Train run
train_run=full2

# Data Path
data=$repo/nn/$nn_name/$nn_name.yaml

# Weights Path
weights=$repo/nn/$nn_name/runs/train/full1/weights/best.pt

# Hyperparameters
imgsz=256
batch=1
epochs=1


# --------------------------- DO NOT EDIT --------------------------- 
# YOLOv5 train file
train=~/yolov5/train.py

# Project(NN) path (local and wandb)
project=$repo/nn/$nn_name

# Run relative path (relative to project)
run=runs/train/$train_run

# echo repo: $repo
# echo nn_name: $nn_name
# echo train_run: $train_run
# echo data: $data
# echo weights: $weights
# echo train: $train
# echo project: $project
# echo run: $run



# ------------------------ EDIT if necessary ------------------------ 
# Train It!
python3 $train  --data $data --weights $weights --imgsz $imgsz --batch $batch --epochs $epochs --project $project --name $run