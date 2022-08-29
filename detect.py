# This file imports yolov5.detect after sys.append the yolov5 folder
# It assumes yolov5 folder is in the same directory as this project

import sys
from pathlib import Path

try:
    yolov5_location = Path(__file__).parent.parent
    sys.path.append(str(yolov5_location))
    from yolov5.detect import run
except:
    print("Could not find YOLOv5 folder!")


def detect(weights, source, data, imgsz,
           conf_thres, iou_thres, save_txt, save_conf,
           project, name, exist_ok):
    """Calls `run` from `detect.py`

    Args:
        weights:  model.pt path(s)
        source:  file/dir/URL/glob, 0 for webcam
        data:  dataset.yaml path (dataset info)
        imgsz:  inference size (height, width)
        conf_thres:  confidence threshold
        iou_thres:  NMS IOU threshold
        save_txt:  save results to *.txt
        save_conf:  save confidences in --save-txt labels
        project:  save results to project/name
        name:  save results to project/name
        exist_ok:  existing project/name ok, do not increment
    """
    run(weights=weights,
        source=source,
        data=data,
        imgsz=(imgsz, imgsz),
        conf_thres=conf_thres,
        iou_thres=iou_thres,
        save_txt=save_txt,
        save_conf=save_conf,
        project=project,
        name=name,
        exist_ok=exist_ok)


if __name__ == "__main__":
    # ---------- EDIT ME ----------
    data = "" # "/home/alexandre/therapy-aid-tool/nn/3objs/3objs.yaml"
    weights = "" # "/home/alexandre/therapy-aid-tool/nn/3objs/runs/full1/train/weights/best.pt"
    source = "" # "/home/alexandre/therapy-aid-tool/sample_data/asd5.mp4"

    imgsz = "" # 256
    conf_thres = "" # 0.75
    iou_thres = "" # 0.45
    save_txt = "" # True
    save_conf = "" # True
    exist_ok = "" # True

    project = "" # "/home/alexandre/therapy-aid-tool/nn/3objs"
    name = "" # "runs/full1/test/insight"
    # ------------------------------
    detect(weights, source,
           data, imgsz,
           conf_thres, iou_thres,
           save_txt, save_conf,
           project, name,
           exist_ok)
