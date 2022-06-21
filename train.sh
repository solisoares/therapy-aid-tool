# Train any Neural Network (NN) available in nn folder

# --- EDIT ---
# NN name (project name, local and wandb)
nn_name=3objs

# Train name (run name)
train_name=full1

# Data Path
data=/home/alexandre/asd-research/nn/$nn_name/$nn_name.yaml

# Weights Path
weights=/home/alexandre/asd-research/nn/$nn_name/runs/train/$train_name/weights/best.pt

# Hyperparameters
imgsz=256
batch=1
epochs=1


# --- DO NOT EDIT --- 
# YOLOv5 train file
train=~/yolov5/train.py

# Project(NN) path (local and wandb)
project=/home/alexandre/asd-research/nn/$nn_name

# Run path
run=runs/train/$train_name


# --- EDIT if necessary ---
# Train It!
python3 $train  --data $data --weights $weights --imgsz $imgsz --batch $batch --epochs $epochs --project $project --name $run