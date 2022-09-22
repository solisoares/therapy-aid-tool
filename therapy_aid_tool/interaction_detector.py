from __future__ import annotations

import os
from pathlib import Path

from configparser import ConfigParser

from collections import defaultdict

from typing import List, Tuple

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


class BBox:
    """Represents a Bounding Box prediction made by YOLOv5
    """

    def __init__(self, pred: Tuple) -> None:
        """Initializes the BBox

        A BBox prediction has two components, a class and the parameters 
        of the bbox (x, y, w, h, conf).
            x, y: center point of the bbox in the frame (float 0 -> 1)
            w, h: width and height of the bbox (float 0 -> 1)
            conf: confidence level of the bbox prediction.

        Args:
            pred (Tuple): Bounding Box Prediction, (cls, [x, y, w, h, conf])
        """
        self.pred = pred
        self.cls = self.pred[0]
        self.xywhc = self.pred[1]
        self.create_corners()

    def create_corners(self):
        """Create the BBox corners x1, x2, y1, y2
        """
        if self.xywhc:
            self.x, self.y, self.w, self.h, self.conf = self.xywhc
            self.x1 = self.x - self.w / 2
            self.x2 = self.x + self.w / 2
            self.y1 = self.y - self.h / 2
            self.y2 = self.y + self.h / 2

    def niou(self, other: BBox):
        """Normalized IoU

        This implements (Area1 ∩ Area2) / min(Area1, Area2)

        Args:
            other (BBox): The other bounding box to check for NIoU

        Returns:    
            TODO
        """
        pass

    def is_overlapping(self, other: BBox):
        """Checks if this BBox is overlapping the another

        Args:
            other (BBox): The other BBox to check overlapping

        Returns:
            bool: Whether or not they it is overlapping
        """
        if self.xywhc and other.xywhc:
            return (self.x1 < other.x2
                    and self.y1 < other.y2
                    and other.x1 < self.x2
                    and other.y1 < self.y2)
        return False


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
        list: Predictions for each class. Key, Value = class, [x,y,w,h,conf] | None
            Example: ((0, [x, y, w, h, conf]), (1, [x, y, w, h, conf]), (2, None), ...}
    """
    # Get predictions as list of lists
    preds = results.xywhn[0].tolist()

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

    return list(preds_dict.items())


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
