#!/usr/bin/bash

# Darknet
darknet='/home/alexandre/darknet/build_release/darknet'

# Project
project='/home/alexandre/asd-research/nn/3objs'
data=$project/'data.txt'
cfg=$project/'yolov4.cfg'
weights=$project/'backup/yolov4_6000.weights'

# Train it
$darknet detector train $data $cfg $weights -clear #> $project/'training.log'
# $darknet detector train $data $cfg -map | tee $project/'training.log'
