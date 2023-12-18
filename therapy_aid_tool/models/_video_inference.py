from __future__ import annotations

from pathlib import Path
from configparser import ConfigParser

from typing import Tuple

import torch
import math

import requests

THIS_FILE = Path(__file__).resolve()
THIS_DIR = THIS_FILE.parent
ROOT = THIS_FILE.parents[2]
MODELS_DIR = ROOT / "models"

# Read config file
CFG_FILE = THIS_DIR.parent / "detect.cfg"
PARSER = ConfigParser()
PARSER.read(CFG_FILE)

# Configs
YOLO_VERSION = "v7.0"
YOLO_REPO = "ultralytics/yolov5:"+YOLO_VERSION  # currently this is the latest version we tested
DEFAULT_MODEL_WEIGHTS = ROOT / PARSER.get("yolov5", "weights")
DEFAULT_MODEL_SIZE = PARSER.getint("model", "size")

def download_weights(save_location: Path):
    """Download pre trained weights from `therapy-aid-nn` v1.0.0 repo release

    The name of the weights to download is the filename content in the `save_location`
    All the weights available are in the keys of the `urls` dictionary bellow

    Args:
        save_location (Path): Location to save the weights
    """
    weights_name = save_location.name

    urls = {
        "full1-yolov5m-img256-bs1.pt": "https://github.com/solisoares/therapy-aid-nn/releases/download/v1.0.0/full1-yolov5m-img256-bs1.pt",
        "full1-yolov5m-img512-bs1.pt": "https://github.com/solisoares/therapy-aid-nn/releases/download/v1.0.0/full1-yolov5m-img512-bs1.pt",
        "full1-yolov5n6-img1280-bs1.pt": "https://github.com/solisoares/therapy-aid-nn/releases/download/v1.0.0/full1-yolov5n6-img1280-bs1.pt",
        "full1-yolov5s-img256-bs1.pt": "https://github.com/solisoares/therapy-aid-nn/releases/download/v1.0.0/full1-yolov5s-img256-bs1.pt",
        "full1-yolov5s-img512-bs16.pt": "https://github.com/solisoares/therapy-aid-nn/releases/download/v1.0.0/full1-yolov5s-img512-bs16.pt",
        "full1-yolov5s-img640-bs1.pt": "https://github.com/solisoares/therapy-aid-nn/releases/download/v1.0.0/full1-yolov5s-img640-bs1.pt",
        "full1-yolov5x-img256-bs1.pt": "https://github.com/solisoares/therapy-aid-nn/releases/download/v1.0.0/full1-yolov5x-img256-bs1.pt",
    }

    req = requests.get(urls[weights_name])
    with open(save_location, "wb") as f:
        f.write(req.content)


def load_model(user_model_name:str=DEFAULT_MODEL_WEIGHTS, conf_th=0.75, iou_th=0.45):
    """Loads the best trained model

    Args:
        user_model_name (str, optional): Used with custom weights. Name of the model to be loaded.
        conf_th (float, optional): Defaults to 0.75.
        iou_th (float, optional): Defaults to 0.45.

    Returns:
        _type_: Model loaded.
        int: Size of the image used in finetuning of model loaded.
    """
    model_weights = ""
    model_size = 0
    model = None
    if user_model_name == DEFAULT_MODEL_WEIGHTS:
        model_weights = user_model_name
        model_size = DEFAULT_MODEL_SIZE
        # Download weights if they do not exist already
        if not model_weights.is_file():
            download_weights(model_weights)
    else: # Using custom weights
        custom_parser = ConfigParser()
        custom_parser.read(MODELS_DIR / user_model_name / "model_configs.cfg")
        model_size = custom_parser.getint("model", "size")
        model_weights = MODELS_DIR / user_model_name / "weights" / "best.pt"

    # Model
    model = torch.hub.load(
        repo_or_dir=YOLO_REPO,
        model="custom",
        path=model_weights,
        source="github"
    )
    model.conf = conf_th
    model.iou = iou_th
    return (model, model_size)

def preds_from_torch_results(results, frame_width, frame_height):
    """Return the best predictions for each clasS from the torch results of a model

    When a model runs on an image or a video frame, the `results` can return information about
    xmin, ymin, xmax, ymax, confidence, class ID & class name values for each prediction made. For a not normalized return we look at
    the `results.pandas().xyxy[0]` generated from the model that comes in form of a Pandas dataframe.

    This function gets xmin, ymin, xmax, ymax, confidence, class ID & class name values for each prediction, and, for each class,
    returns the normalized values of x, y, w, h & confidence of the predictions with highest conf score. The classes considered are 
    'toddler', 'caretaker', and 'plusme', and the values for each class are given in this same order.

    results.pandas().xyxy[0] example output:

              xmin        ymin         xmax         ymax      confidence   class    name  
        0  247.064941  418.516083   805.068726  1037.818359    0.937590      0     toddler 
        1  517.709351  422.175903   751.586731   766.561584    0.909404      2     plusme
        2  575.854736   40.794495  1591.923706   843.149048    0.899090      1     caretaker

    Args:
        results: Torch predictions for a frame.
        frame_width: The width of the frame in which predictions were made.
        frame_height: The height of the frame in which predictions were made.

    Returns:
        list: Predictions for each class (['toddler','caretaker','plusme'], in this order). Key, Value = class, [x,y,w,h,conf] | None
            Example: [('toddler', [x, y, w, h, conf]), ('caretaker', [x, y, w, h, conf]), ('plusme', None)]
    """

    class_names = ['toddler','caretaker','plusme']

    # Get predictions as a Pandas dataframe
    preds = results.pandas().xyxy[0].values.tolist()

    # All class numbers initiate with a list with -inf values
    preds_dict = {c: [[float("-inf")] * 5] for c in class_names}

    # Separate predictions according to class name
    for pred in preds:
        if pred[6] in class_names:
            w = (pred[2]-pred[0]) / frame_width # (xmax-xmin) / frame_width
            h = (pred[3]-pred[1]) / frame_height # (ymax-ymin) / frame_height
            x = pred[0]/frame_width + w/2 # xmin/frame_widht + w/2
            y = pred[1]/frame_height + h/2 # ymin/frame_height + h/2
            conf = pred[4]
            preds_dict[pred[6]].append([x,y,w,h,conf])

    # Get predictions with highest conf for each class
    for name in class_names:
        preds_dict[name] = sorted(preds_dict[name], key=lambda x: x[-1])[-1]
        # the ones that still have -inf turn to None
        if float("-inf") in preds_dict[name]:
            preds_dict[name] = None

    return list(preds_dict.items())


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

    def __bool__(self):
        return self.conf != None

    def create_corners(self):
        """Create the BBox corners x1, x2, y1, y2
        """
        if self.xywhc:
            self.x, self.y, self.w, self.h, self.conf = self.xywhc
            self.x1 = self.x - self.w / 2
            self.x2 = self.x + self.w / 2
            self.y1 = self.y - self.h / 2
            self.y2 = self.y + self.h / 2
        else:
            self.x, self.y, self.w, self.h, self.conf = None, None, None, None, None
            self.x1 = None,
            self.x2 = None,
            self.y1 = None,
            self.y2 = None,

    def rectangular_area(self, x1, x2, y1, y2):
        return (x2 - x1) * (y2 - y1)

    def intersection(self, other: BBox):
        # Intersection corners
        x1 = max(self.x1, other.x1)
        y1 = max(self.y1, other.y1)
        x2 = min(self.x2, other.x2)
        y2 = min(self.y2, other.y2)

        area = self.rectangular_area(x1, x2, y1, y2)
        return area

    def niou(self, other: BBox):
        """Normalized IoU

        This implements (Area1 ∩ Area2) / min(Area1, Area2)

        Args:
            other (BBox): The other bounding box to check for NIoU

        Returns:    
            float: the value of the normalized iou
        """
        niou = 0
        try:
            if self.is_overlapping(other):
                intersection_area = self.intersection(other)
                min_area = min(
                    self.rectangular_area(self.x1, self.x2, self.y1, self.y2),
                    other.rectangular_area(
                        other.x1, other.x2, other.y1, other.y2)
                )
                niou = intersection_area / min_area
            return niou
        except:
            return math.nan

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
        raise Exception("Some bounding box was not detected")
