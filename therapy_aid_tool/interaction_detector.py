from __future__ import annotations

import os
from pathlib import Path

from configparser import ConfigParser

from collections import defaultdict

from typing import List

from therapy_aid_tool.utils.video import get_video_frames_count

import cv2
import torch


THIS_FILE = Path(__file__)
THIS_DIR = THIS_FILE.parent

# Read config file
CFG_FILE = THIS_DIR / "detect.cfg"
PARSER = ConfigParser()
PARSER.read(CFG_FILE)

# Configs
YOLO_PATH = PARSER.get("yolov5", "path")
MODEL_WEIGHTS = PARSER.get("yolov5", "weights")
MODEL_SIZE = PARSER.getint("model", "size")


def preds_from_torch_results(results, n_classes):
    """Return the best predictions for each clas from the torch results of a model

    When a model runs on an image or a video frame, the `results` can return information about
    x, y, w, h, conf & class values for each prediction made. For a normalized return we look at
    the `results.xywhn` generated from the model tha comes in form of a List[Tensor].

    This function gets x, y, w, h, conf & class values for each prediction, and for each class,
    return the prediction with highest conf score.

    results.xywhn example output:

                     x        y        w        h       conf     class
                 -----------------------------------------------------
        [tensor([[0.50623, 0.75267, 0.24268, 0.44551, 0.89929, 0.00000],
                 [0.72019, 0.65559, 0.28206, 0.54527, 0.86348, 1.00000],
                 [0.60743, 0.81043, 0.08960, 0.21956, 0.83557, 2.00000]],
                 device='cuda:0')]

    Args:
        results: Torch predictions for a frame
        n_classes (int): Number of classes. Used to create template for lacking predictions

    Returns:
        tuple: Predictions for each class. Key, Value = class, [x,y,w,h,conf] | None
            Example: ((0, [x, y, w, h, conf]), (1, [x, y, w, h, conf]), (2, None), ...}
    """
    # Get predictions as list of lists
    preds = results.xywhn.pop().tolist()

    # All class numbers initiate with a list with -inf values
    preds_dict = {c: [[float("-inf")] * 5] for c in range(n_classes)}

    # Separete predictions according to class number
    for *xywhc, c in preds:
        preds_dict[c].append(xywhc)

    # Get predictions with highest conf for each class
    for c in range(n_classes):
        preds_dict[c] = sorted(preds_dict[c], key=lambda x: x[-1])[-1]
        # the ones that still have -inf turn to None
        if float("-inf") in preds_dict[c]:
            preds_dict[c] = None

    return tuple(preds_dict.items())


class BBox:
    def __init__(self, pred: List[float]) -> None:
        self.pred = pred  # One torch prediction is (cls, [x, y, w, h, conf])
        if self.pred[-1] != None:
            self.cls, (self.x, self.y, self.w, self.h, self.conf) = pred
            self.xmin = self.x - self.w / 2
            self.xmax = self.x + self.w / 2
            self.ymin = self.y - self.h / 2
            self.ymax = self.y + self.h / 2
        else:
            self.cls, self.x, self.y, self.w, self.h, self.conf = [0]*6

    def iou(self, other: BBox):
        pass

    def is_overlapping(self, other: BBox):
        if self.pred[-1] and other.pred[-1]:
            return (
                self.xmin < other.xmax
                and self.ymin < other.ymax
                and other.xmin < self.xmax
                and other.ymin < self.ymax
            )
        return False


def load_model(conf_th=0.75, iou_th=0.45):
    """Loads the best trained model

    Args:
        conf_th (float, optional): _description_. Defaults to 0.75.
        iou_th (float, optional): _description_. Defaults to 0.45.

    Returns:
        _type_: _description_
    """
    # Model
    model = torch.hub.load(
        repo_or_dir=YOLO_PATH,
        model="custom",
        path=MODEL_WEIGHTS,
        source="local"
    )
    model.conf = conf_th
    model.iou = iou_th
    return model


def interaction_detector(in_video: str, n_classes=3):

    model = load_model()
    cap = cv2.VideoCapture(in_video)
    total_frames = get_video_frames_count(in_video)
    interactions = defaultdict(list)
    for i in range(total_frames):
        _, frame = cap.read()
        results = model(frame[:, :, ::-1], size=MODEL_SIZE)
        preds = preds_from_torch_results(results, n_classes)
        
        td = BBox(preds[0])
        ct = BBox(preds[1])
        pm = BBox(preds[2])
        
        interactions["td_ct"].append(td.is_overlapping(ct))
        interactions["td_pm"].append(td.is_overlapping(pm))
        interactions["ct_pm"].append(ct.is_overlapping(pm))

    return interactions
