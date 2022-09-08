# This file imports `run` from `yolov5.detect`
# It assumes yolov5 folder inside this project directory

from configparser import ConfigParser

try:
    from yolov5.detect import run
except:
    print("Could not find YOLOv5! Make sure its folder is inside this project!")


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
    # Get detect.cfg configurations
    config = ConfigParser()
    config.read('detect.cfg')

    data = config.get('load', 'data')
    weights = config.get('load', 'weights')
    source = config.get('load', 'source')

    imgsz = config.getint('options', 'imgsz')
    conf_thres = config.getfloat('options', 'conf_thres')
    iou_thres = config.getfloat('options', 'iou_thres')
    save_txt = config.getboolean('options', 'save_txt')
    save_conf = config.getboolean('options', 'save_conf')
    exist_ok = config.getboolean('options', 'exist_ok')

    project = config.get('run-location', 'project')
    name = config.get('run-location', 'name')

    # Perform detection
    detect(weights, source,
           data, imgsz,
           conf_thres, iou_thres,
           save_txt, save_conf,
           project, name,
           exist_ok)