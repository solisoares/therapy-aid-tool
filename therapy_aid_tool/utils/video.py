import os
from pathlib import Path
import cv2


def get_video_frames_count(source: str):
    """Return the total frames a video has

    Args:
        source (str): Video path

    Returns:
        int: Total frames count
    """
    cap = cv2.VideoCapture(source)
    frames_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return frames_count


def get_video_fps(source: str):
    cap = cv2.VideoCapture(source)
    fps = float(cap.get(cv2.CAP_PROP_FPS))
    cap.release()
    return fps
