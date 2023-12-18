# This file is a modification of https://github.com/solisoares/therapy-aid-nn/blob/main/scripts/download_labelbox_images_and_labels.py
# and https://github.com/ultralytics/JSON2YOLO/blob/master/labelbox_json2yolo.py

from pathlib import Path
import random

import labelbox
import requests
from PIL import Image
from stqdm import stqdm

from therapy_aid_tool.models._video_inference import (
    ROOT
)

def _make_dirs(dir):
    """Create folders"""
    dir = Path(dir)
    if dir.exists():
        raise OSError(
            "This directory already exists. Remove it or choose another destination"
        )
    
    dirs_dataset = ["train", "valid", "test"]
    subdirs = ["images","labels"]
    dir.mkdir(parents=True, exist_ok=True)
    for d in dirs_dataset:
        p = dir / d
        p.mkdir()
        for sd in subdirs:
            p = dir / d / sd
            p.mkdir(parents=True, exist_ok=True)
    
    return dir

def _download_raw_content(api_key: str, proj_id: str):
    """Download labels and images url as json array

    Args:
        api_key (str): Labelbox API key
        proj_id (str): Labelbox Project ID

    Returns:
        raw_content (List): Raw content of labels and images as a json array
    """
    client = labelbox.Client(api_key)
    project = client.get_project(proj_id)
    export_task = project.export_v2(params={ # json as list (json array)
	"data_row_details": True,
	"metadata_fields": True,
	"attachments": True,
	"project_details": True,
	"performance_details": True,
	"label_details": True,
	"interpolated_frames": True
    })
    raw_content = export_task.wait_till_done()
    
    if export_task.errors:
        print(export_task.errors)

    raw_content = export_task.result

    return raw_content

def download_images_and_labels(api_key: str, proj_id: str, out_path: Path, dataset_perc: tuple):
    """Download images and YOLO formated labels from Labelbox to train, valid and test folders and creates a .yaml file
    indicating the paths to them. 

    Args:
        api_key (str): Labelbox API key
        proj_id (str): Labelbox Project ID
        out_path (Path): Location to save images and labels
        dataset_perc (tuple): Percentage of the dataset to be placed in each set, in the sequence (train, valid, test)
    """
    # Validate input values
    if not all((api_key, proj_id)):
        raise NameError(
            "Set LABELBOX_API and/or PROJECT_ID inside this file to proceed"
        )
    if dataset_perc[0]+dataset_perc[1]+dataset_perc[2] != 100:
        raise ValueError ("Invalid train, valid and test percentages")

    names = []  # class names
    save_dir = _make_dirs(out_path)

    # Download labels and images url as json array
    data = _download_raw_content(api_key, proj_id)
    random.shuffle(data)

    # Limit indexes in the list of data to define the set each data will be placed
    # If 0 <= index <= train_limit_index: Place it in training set
    # If train_limit_index < index <= valid_limit_index: Place it in validation set
    # If valid_limit_index < index: Place it in testing set
    train_limit_index = len(data) * dataset_perc[0]/100
    valid_limit_index = len(data) * (dataset_perc[0]+dataset_perc[1])/100
    img_index = -1

    # TODO: Change from stqdm to another alternative to not mix frontend and backend of the app
    for img in stqdm(data, desc=f"Downloading images and labels"):
        im_path = img["data_row"]["row_data"]
        im = Image.open(
            requests.get(im_path, stream=True).raw
            if im_path.startswith("http")
            else im_path
        )  # open
        width, height = im.size  # image size

        # Defines the set the data will be placed
        img_index += 1
        folder_set = "test"
        if img_index <= train_limit_index:
            folder_set = "train"
        elif img_index <= valid_limit_index:
            folder_set = "valid"

        label_path = (
            save_dir / folder_set / "labels" / Path(img["data_row"]["external_id"]).with_suffix(".txt").name
        )
        image_path = save_dir / folder_set / "images" / img["data_row"]["external_id"]
        im.save(image_path, quality=95, subsampling=0)

        for lb in img["projects"][proj_id]["labels"]:
            if "objects" in lb["annotations"]:
                for label in lb["annotations"]["objects"]:
                    # box
                    # top, left, height, width
                    top, left, h, w = label["bounding_box"].values()
                    xywh = [
                        (left + w / 2) / width,
                        (top + h / 2) / height,
                        w / width,
                        h / height,
                    ]  # xywh normalized

                    # class
                    cls = label["name"]  # class name
                    if cls not in names:
                        names.append(cls)

                    # YOLO format (class_index, xywh)
                    line = names.index(cls), *xywh
                    with open(label_path, "a") as f:
                        f.write(("%g " * len(line)).rstrip() % line + "\n")

    # Creates data.yaml file
    yaml_path = save_dir / "data.yaml"
    with yaml_path.open(mode='w') as file:
        file.write(  "path: "+(str)(Path(__file__).parent / save_dir)+"\n"\
                    +"train: train/images\n"\
                    +"val: valid/images\n"\
                    +"test: test/images\n"\
                    +"nc: "+(str)(len(names))+"\n"\
                    +"names: [")
        str_names = ""
        for name in names:
            str_names += "'"+name+"',"
        str_names = str_names[:-1]+"]"
        file.write(str_names)

def download_from_labelbox(labelbox_api:str, project_id:str, train_perc:int, valid_perc:int, test_perc:int, dataset_name:str) -> (bool,Path):
    """Download a dataset right from Labelbox.

    Args:
        labelbox_api (str): The user's API key from Labelbox.
        project_id (str): The ID from Labelbox project.
        train_perc (int): Percentage of the dataset to be placed in the training set.
        valid_perc (int): Percentage of the dataset to be placed in the validation set.
        test_perc (int): Percentage of the dataset to be placed in the testing set.
        dataset_name (str): The name for the dataset to be downloaded.
        
    Returns:
        bool: True if the operation was successfull.
        Path: The path where the dataset was saved.
    """
    out_path = ROOT / "datasets" / dataset_name
    download_images_and_labels(labelbox_api, project_id, out_path, (train_perc,valid_perc,test_perc))
    return (True, out_path)