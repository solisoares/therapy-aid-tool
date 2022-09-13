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


def save_video_labels_template(source: str):
    """Save empty labels for frames without detection

    This is necessary because empty frames do not generate a
    labels file

    Args:
        source (str): Video path
    """
    frames_count = get_video_frames_count(source)
    dir_name = os.path.dirname(source)
    source_name = Path(source).stem

    for frame in range(1, frames_count + 1):
        label = os.path.join(dir_name, "labels", source_name + f"_{frame}.txt")
        # If the label do not exist, create it as an empty file
        if not os.path.isfile(label):
            with open(label, "w") as f:
                f.write("")
