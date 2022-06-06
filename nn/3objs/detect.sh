#!/usr/bin/bash

# Darknet
darknet='/home/alexandre/darknet/build_release/darknet'

# Project ---------------------------------------------------------------
project='/home/alexandre/asd-research/nn/3objs'
data=$project/'data.txt'
cfg=$project/'yolov4.cfg'
weights=$project/'backup/yolov4_best.weights'
# -----------------------------------------------------------------------

# Detect image (input image - output predictions.jpg)
# input="/home/alexandre/asd-research/nn/3objs/imgs/asd1-132.jpg"
# $darknet detector test $data $cfg $weights $input 

# Detect list of images (input list in txt - output json or txt)
input="/home/alexandre/asd-research/nn/3objs/train.txt"
output="/home/alexandre/asd-research/nn/3objs/test_data/train_results/train_result.json"
$darknet detector test $data $cfg $weights -out $output -dont_show < $input   # -ext_output -dont_show
# $darknet detector test $data $cfg $weights -dont_show -ext_output < $input > $output

# Detect video (input video - output video)
# input='/home/alexandre/asd-research/nn/3objs/test_data/train_video.avi
# output="/home/alexandre/asd-research/nn/3objs/test_data/train_video_result.avi"
# $darknet detector demo $data $cfg $weights $input -out_filename $output #-thresh 0.5  # -dont_show -thresh 

# Check accuracy mAP@IoU=0.x
# $darknet detector map $data $cfg $weights #-iou_thresh 0.5

# Valid: used to evaluate AP on the MS COCO evaluation server
