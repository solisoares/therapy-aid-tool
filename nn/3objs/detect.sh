#!/usr/bin/bash

# Darknet
darknet='/home/alexandre/darknet/build_release/darknet'

# Project ---------------------------------------------------------------
project='/home/alexandre/asd-research/nn/3objs'
data=$project/'data.txt'
cfg=$project/'yolov4.cfg'
weights=$project/'backup/yolov4_best.weights'

# Input (image, list of images or video)
input='/home/alexandre/asd-research/nn/3objs/test_data/test_video.avi'

# Output (.json or video)
output="/home/alexandre/asd-research/nn/3objs/test_data/test_video_result50.avi"
# -----------------------------------------------------------------------

# Detect image
# $darknet detector test $data $cfg $weights $input 

# # Detect list of images
# $darknet detector test $data $cfg $weights -out $output < $input  # -ext_output -dont_show

# Detect video
$darknet detector demo $data $cfg $weights $input -out_filename $output -thresh 0.5  # -dont_show -thresh 

# # Check accuracy mAP@IoU=0.x
# $darknet detector map $data $cfg $weights -iou_thresh 0.5

# Valid: used to evaluate AP on the MS COCO evaluation server
