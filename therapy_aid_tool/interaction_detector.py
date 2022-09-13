from __future__ import annotations

import os
from pathlib import Path

from stringprep import in_table_a1
from typing import List

import cv2

from .utils.natural_sort import natural_sort_key
from .utils.filepaths import get_filepaths_from_dir
from .utils.video import save_video_labels_template


def get_file_preds(filepath: str):
    """Return a sorted list of a file's predictions

    Single prediction pattern: cls x y w h [conf]
    File's predictions:
        cls x y w h [conf]
        cls x y w h [conf]
        ...
    Function return: ['0 x y w h [conf]',
                      '1 x y w h [conf]',
                      '2 x y w h [conf]', 
                       ... ]

    Args:
        filepath (str): Path to file

    Returns:
        preds (List[str]):  Sorted predictions
    """

    with open(filepath, 'r') as f:
        preds = sorted(f.read().splitlines())
        return preds


class BBox:
    def __init__(self, pred: str) -> None:
        self.pred = pred
        if self.pred:
            (self.cls, self.x, self.y, self.w, self.h, self.conf) = self.__split_pred()
            self.xmin = self.x - self.w/2
            self.xmax = self.x + self.w/2
            self.ymin = self.y - self.h/2
            self.ymax = self.y + self.h/2

    def __split_pred(self):
        return (float(s) for s in self.pred.split(" "))

    def iou(self, other: BBox):
        pass

    def is_overlapping(self, other: BBox):
        if self.pred and other.pred:
            return (self.xmin < other.xmax
                    and self.ymin < other.ymax
                    and other.xmin < self.xmax
                    and other.ymin < self.ymax)
        return False


def get_3preds(preds: List[str]):
    """Return 3 predictions even though there
    is less or more in each predictions file.

    Args:
        preds (List[str]): File predictions in form of a list o strings

    Returns:
        predictions: 3 predictions, each one with or without ('') content
    """
    # Initialize each class prediction
    pred0, pred1, pred2 = [''], [''], ['']
    # Get together repeated class predictions
    for pred in preds:
        if pred[0] == '0':
            pred0.append(pred)  # ['0...','0...','0...', ...]
        if pred[0] == '1':
            pred1.append(pred)
        if pred[0] == '2':
            pred2.append(pred)
    # Choose prediction with higher conf among repeated ones
    pred0 = get_higher_conf_pred(pred0)
    pred1 = get_higher_conf_pred(pred1)
    pred2 = get_higher_conf_pred(pred2)
    return pred0, pred1, pred2


def get_higher_conf_pred(repeated_preds: List[str]):
    """Return the prediction with higher conf among repeated ones

    It sorts a list based on the last element that is divided by space
    due to a lambda function

    Args:
        repeated_preds (List[str]): A list with repeated predictions

    Returns:
        [higher_conf_pred]: The higher conf prediction inside a list
    """
    sorted_preds = sorted(
        repeated_preds,
        key=lambda x: x.split(" ")[-1]
    )
    higher_conf_pred = sorted_preds[-1]
    return higher_conf_pred


# # fp1 = 'labels/test'  # cls: None
# # fp1 = 'labels/test_video_9.txt'  # cls: 2
# # fp1 = 'labels/test_video_33.txt'  # cls: 0 0 2

# fp1 = 'context_parser/labels/test_video_9.txt'
# preds = get_3preds(get_file_preds(fp1))

# td = BBox(preds[0])
# ct = BBox(preds[1])
# pm = BBox(preds[2])
# # td,ct,pm = get_3preds(get_file_preds(fp1))

# print(td.is_overlapping(ct))
# print(td.is_overlapping(pm))
# print(ct.is_overlapping(pm))


# ---------------------------------------------------------
def interaction_parser(
        detection_dir: Path,
        in_video: str,
        out_video: str):

    # paths used
    in_video = os.path.join(detection_dir, in_video)
    out_video = os.path.join(detection_dir, out_video)

    save_video_labels_template(in_video)    
    labels = get_filepaths_from_dir(
        os.path.join(detection_dir, 'labels'), key=natural_sort_key)

    cap = cv2.VideoCapture(in_video)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    writer = cv2.VideoWriter(
        out_video, cv2.VideoWriter_fourcc(*'DIVX'), 20, (width, height))

    count = 0
    while(True):
        ret, frame = cap.read()  # reads 1 frame from video
        if not ret:
            break
        
        preds = get_3preds(get_file_preds(labels[count]))
        td = BBox(preds[0])
        ct = BBox(preds[1])
        pm = BBox(preds[2])
        td_ct = td.is_overlapping(ct)  # True/False
        td_pm = td.is_overlapping(pm)
        ct_pm = ct.is_overlapping(pm)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, f'frame: {count+1}',
                    (50, 200), font,
                    0.75, (0, 255, 255),
                    2, cv2.LINE_4)
        cv2.putText(frame, f'Interaction*:',
                    (50, 250), font,
                    0.75, (255, 0, 0),
                    2, cv2.LINE_4)
        cv2.putText(frame, f' toddler-caretaker: {td_ct}',
                    (50, 300), font,
                    0.75, (255, 0, 0),
                    2, cv2.LINE_4)
        cv2.putText(frame, f' toddler-plusme: {td_pm}',
                    (50, 350), font,
                    0.75, (255, 0, 0),
                    2, cv2.LINE_4)
        cv2.putText(frame, f' caretaker-plusme: {ct_pm}',
                    (50, 400), font,
                    0.75, (255, 0, 0),
                    2, cv2.LINE_4)
        writer.write(frame)

        # Display the resulting frame
        cv2.imshow('video', frame)
        # creating 'q' as the quit button for the video
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        count += 1

    cap.release()
    writer.release()
    cv2.destroyAllWindows()
