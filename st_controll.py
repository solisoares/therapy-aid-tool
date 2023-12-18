import streamlit as st

from copy import deepcopy
from io import BufferedReader
from pathlib import Path
from typing import Union
from zipfile import ZipFile

import numpy as np
import matplotlib.pyplot as plt

from therapy_aid_tool.models.toddler import Toddler
from therapy_aid_tool.models.video import Video
from therapy_aid_tool.models.session import Session
from therapy_aid_tool.models.yolo_finetuning import (finetune_yolo_model, ROOT, MODELS_DIR)
from therapy_aid_tool.models.download_labelbox_dataset import download_from_labelbox

from therapy_aid_tool.DAOs.toddler_dao import ToddlerDAO
from therapy_aid_tool.DAOs.video_dao import VideoDAO
from therapy_aid_tool.DAOs.session_dao import SessionDAO


DATASETS_DIR = ROOT / "datasets"

DATABASE_DIR = ROOT/"database"
DATABASE = DATABASE_DIR/"sessions.db"

VIDEOS_DIR = DATABASE_DIR/"videos"

# ==================================================
# Utils

def save_user_file(file: BufferedReader, location: Union[str, Path]):
    """Save the user uploaded file

    The type of the streamlit uploaded file is a "UploadedFile" but respects
    the Buffer protocol

    Args:
        file (BufferedReader): The user uploaded file to the streamlit app
        location (Union[str, Path]): Where to save this video
    """
    with open(location, "wb") as f:
        f.write(file.read())

# ==================================================
# Dataset import

def existing_dataset(dataset_name:str) -> (bool, str):
    """Verifies if a specific dataset already exists in models folder. 

    Returns:
        bool: Returns True if the dataset alrady exists.
        str: A non-expty warning message, if the dataset exists.
    """
    path = DATASETS_DIR / dataset_name
    if path.exists():
        return (True, "The dataset already exists.")
    return (False,"")

def download_dataset_from_labelbox(labelbox_api:str, project_id:str, train_perc:int, valid_perc:int, test_perc:int, dataset_name:str) -> (bool,Path):
    """Calls the module of download of a dataset right from Labelbox.

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
    return download_from_labelbox(labelbox_api, project_id, train_perc, valid_perc, test_perc, dataset_name)

def create_dataset_from_zip(dataset:BufferedReader):
    """Creates, from a ZIP file, a folder in the datasets folder with content for a dataset.

    Args:
        dataset (BufferedReader): The uploaded ZIP file for a dataset.
    """
    path_zip = ROOT / dataset.name
    save_user_file(dataset, path_zip)

    if not DATASETS_DIR.is_dir():
        DATASETS_DIR.mkdir()
    dest_path = DATASETS_DIR / dataset.name[:-4]
    dest_path.mkdir()
    with ZipFile(dataset.name, 'r') as zip_obj:
        zip_obj.extractall(path=dest_path)

    path_zip.unlink()

# ==================================================
# Model training, import and export

def finetune_yolo(dataset_name:str, train_model_name:str, image_size:int, num_epochs:int, batch_size:int, model_name:str) -> (bool,str):
    """Calls the module of YOLO model finetuning.

    Args:
        dataset_name (str): The name of the dataset to be used in finetuning.
        train_model_name (str): The name of the finetuned model.
        image_size (int): Size of the image to be used in finetuning.
        num_epochs (int): Number of epochs to be used in finetuning.
        batch_size (int): Size of the batch to be used in finetuning.
        model_name (str): The YOLOv5 base model to be finetuned (i.e. yolov5m.pt, yolov5s.pt, yolov5m.pt, yolov5l.pt or yolov5x.pt).

    Returns:
        bool: True if the finetuning was a success.
        str: If finetunins was not successfull, a non-empty warning message with the error occurred.
    """
    return finetune_yolo_model((DATASETS_DIR / dataset_name), train_model_name, image_size, num_epochs, batch_size, model_name)

def existing_model(model_name:str) -> (bool, str):
    """Verifies if a specific model already exists in models folder. 

    Returns:
        bool: Returns True if the model alrady exists.
        str: A non-expty warning message, if the model exists.
    """
    path = MODELS_DIR / model_name
    if path.exists():
        return (True, "The model already exists.")
    return (False,"")

def default_model_index() -> int:
    """Returns a model name index according to the session state information.

    Returns:
        int: Model name index.
    """
    if "model" in st.session_state and st.session_state.model in model_names():
        return model_names().index(st.session_state.model)
    else:
        return 0

def dataset_names() -> list[str]:
    """Returns the name of all available datasets.

    Returns:
        list[str]: All available datasets.
    """
    datasets = []
    if DATASETS_DIR.is_dir():
        for file_path in DATASETS_DIR.iterdir():
            if file_path.is_dir():
                filename = file_path.parts
                datasets.append(filename[len(filename)-1])
    return datasets

def default_dataset_index() -> int:
    """Returns a dataset name index according to the session state information.

    Returns:
        int: Model dataset index.
    """
    if "dataset" in st.session_state and st.session_state.dataset in dataset_names():
        return dataset_names().index(st.session_state.dataset)
    else:
        return 0

def verify_dataset_folder(dataset_name:str) -> (bool, str):
    """Checks if the dataset folder have the expected format.

    Expected contents:\n
    data.yaml\n
    train\n
        images\n
        labels\n
    valid\n
        images\n
        labels\n
    test\n
        images\n
        labels\n

    Returns:
        bool: Return True if the folder is in the expected format.
        str: Returns a non-empty warning message if the dataset folder isnot in the expected format.
    """
    path = DATASETS_DIR / dataset_name
    if not (path / "data.yaml").is_file():
        return (False, "The file 'data.yaml' does not exist. See 'Train your model' for the correct dataset folder format.")
    folders = ['train','valid','test']
    subfolders = ['images','labels']
    for folder in folders:
        if not (path / folder).is_dir():
            return (False, "The folder '"+folder+"' does not exist. See 'Train your model' for the correct dataset folder format.")
        for subfolder in subfolders:
            if (not (path / folder / subfolder).is_dir()):
                return (False, "The folder '"+subfolder+"' in '"+folder+"' does not exist. See 'Train your model' for the correct dataset folder format.")
    return (True,"")

def create_model_from_zip(model:BufferedReader):
    """Creates, from a ZIP file, a folder in the models folder with content for a model.

    It is assumed that the model uploaded was trained and exported using Therapy Aid Tool.

    Args:
        model (BufferedReader): The uploaded ZIP file for a model exported with Therapy Aid Tool.
    """
    path_zip = ROOT / model.name
    save_user_file(model, path_zip)

    if not MODELS_DIR.is_dir():
        MODELS_DIR.mkdir()
    dest_path = MODELS_DIR / model.name[:-4]
    dest_path.mkdir()
    with ZipFile(model.name, 'r') as zip_obj:
        zip_obj.extractall(path=dest_path)

    path_zip.unlink()

def create_zip_from_model(model_name:str) -> str:
    """Creates a ZIP file containing an available model folder content.

    Returns:
        str: The path were the ZIP file was saved.
    """
    model_path = MODELS_DIR / model_name
    zip_path = ROOT / Path(model_name+".zip")
    with ZipFile(zip_path, 'w') as zip_obj:
        for entry in model_path.rglob("*"):
            zip_obj.write(entry, entry.relative_to(model_path))
    return (str)(zip_path)

# ==================================================
# Model's test performance visualization

def test_image_paths(model_name:str) -> list[str]:
    """Returns the name of all available test images with bounding boxes.

    Returns:
        list[str]: All available test images with bounding boxes.
    """
    imgs_path = []
    test_imgs_dir = MODELS_DIR / model_name / "test_imgs"
    if test_imgs_dir.is_dir():
        detected_imgs = test_imgs_dir / "detected"
        if detected_imgs.is_dir():
            for file_path in detected_imgs.iterdir():
                if file_path.is_file():
                    imgs_path.append(file_path)
    return imgs_path

# ==================================================
# Video inference

def model_names() -> list[str]:
    """Returns the name of all available models.

    Returns:
        list[str]: All available models.
    """
    models = []
    if MODELS_DIR.is_dir():
        for file_path in MODELS_DIR.iterdir():
            if file_path.is_dir():
                filename = file_path.parts
                models.append(filename[len(filename)-1])
    return models

def video_fp_from_toddler_date(toddler: Toddler, date: str):
    """Generate a filepath for a video with the toddler name
    and the date of the therapy session

    Args:
        toddler (Toddler): The toddler in the session
        date (str): The date of the session

    Returns:
        str: The generated video filepath according to toddler.name and date
    """
    filepath = str(VIDEOS_DIR/f"{'-'.join(toddler.name.split())}_{date}.mp4")
    return filepath


def add_session(toddler: Toddler, video: Video, date: str):
    """Add a session to the database

    If any of the three exists (toddler, video, session) in
    the database, the addition is not made and no error or
    exception is returned

    Args:
        toddler (Toddler): The toddler in the session
        video (Video): The video of the session
        date (str): The date of the session
    """
    session = Session(toddler, video, date)
    ToddlerDAO(DATABASE).add(toddler)
    VideoDAO(DATABASE).add(video)
    SessionDAO(DATABASE).add(session)


def toddlers_names():
    """Get a list of all toddlers names

    Returns:
        list[str]: the toddlers' names
    """
    return ToddlerDAO(DATABASE).get_all_names()


def dates_from_name(name: str):
    """Get a list of all sessions dates that a toddler appears
    
    Returns:
        list[str]: The session dates where a toddler appears
    """
    return SessionDAO(DATABASE).get_dates_from_name(name)


def get_session(toddler_name: str, date: str):
    """Get a session
    
    A session can be querrid from toddler and a date
    
    Returns:
        Session: The Session
    """
    return SessionDAO(DATABASE).get(toddler_name, date)


def __sessions_from_name(toddler_name: str):
    """Get list of all the sessions that a toddler is present

    Args:
        toddler_name (str): The name o the toddler   

    Returns:
        list[Session]: The sessions the toddler is present
    """
    return SessionDAO(DATABASE).get_all_from_name(toddler_name)


def __statistics_from_all_sessions(toddler_name: str):
    """Get statistics from all sessions that a toddler is present

    It returns a dictionary of statistics where the keys are
    the three interactions classes (td_ct, td_pm, ct_pm) and
    the value for each key is a dictionary of lists, where
    those keys are the type of statistics and their value a list
    of that statistic over the sessions.

    Return example for 4 existing sessions:
        statistics = {
            'td_ct': {'n_interactions': [int, int, int, int],
                      'min_time': [float, float, float, float],
                      'max_time': [float, float, float, float],
                      'mean_time': [float, float, float, float]},
            'td_pm': ...,
            'ct_pm': ...,
        }

    Args:
        toddler_name (str): The name of the toddler   

    Returns:
        dict[str, dict[str, list[Unknown]]]: The statistics for all sessions
    """
    sessions = __sessions_from_name(toddler_name)
    sessions = sorted(sessions, key=lambda ses: ses.date)
    
    # interactions statisics for each session
    separated_statistics = [session.video.interactions_statistics
                            for session in sessions]

    data_template = {
        "n_interactions": [],
        "total_time": [],
        "min_time": [],
        "max_time": [],
        "mean_time": [],
    }
    statistics = {
        "td_ct": deepcopy(data_template),
        "td_pm": deepcopy(data_template),
        "ct_pm": deepcopy(data_template),
    }

    # Merge separated statistics for a class into lists over the sessions
    for sep_stat in separated_statistics:
        for inter_type, stat_group in sep_stat.items():
            for type_stat, stat_value in stat_group.items():
                statistics[inter_type][type_stat].append(stat_value)
                # Example: statistics['td_ct']['min_time'].append(float)
    return statistics


def plot_sessions_progress(toddler_name: str):
    """Plots the progress of a toddler over the sessions they appear

    On the left y axis, plots about time statistics (min_time, max_time ...).
    On the right y axis, plot about counts (nº of interactions)

    Args:
        toddler_name (str): The name o the toddler
    """
    statistics = __statistics_from_all_sessions(toddler_name)

    titles = {
        'td_ct': 'Toddler-Caretaker',
        'td_pm': 'Toddler-PlusMe',
        'ct_pm': 'Caretaker-PlusMe',
    }

    stat_type = ['n_interactions', 'total_time',
                 'min_time', 'max_time', 'mean_time']
    color_map = plt.get_cmap("hsv")
    colors = dict(zip(stat_type, color_map(np.linspace(0, 1, 6))))

    labels = {
        'n_interactions': 'nº interactions',
        'total_time': 'total time',
        'min_time': 'min time',
        'max_time': 'max time',
        'mean_time': 'mean time',
    }

    n_sessions = len(statistics['td_ct']['n_interactions'])
    x = np.arange(1, n_sessions + 1)

    for inter_type, stat_group in statistics.items():
        fig, ax1 = plt.subplots(figsize=(14, 5))

        for stat_type, values in stat_group.items():
            ax = ax1
            leg_loc = "upper left"
            y_label = "Seconds"
            ax.set_title(titles[inter_type])
            ax.grid()
            ax.set_xlabel("Sessions", loc="center", fontweight="bold")
            ax.set_xticks(range(1, n_sessions + 1))

            if stat_type == "n_interactions":
                ax2 = ax1.twinx()
                ax = ax2
                leg_loc = "upper right"
                y_label = "Count"

            ax.plot(x, values, "o-", alpha=1,
                    color=colors[stat_type],
                    label=labels[stat_type])
            ax.legend(loc=leg_loc)
            ax.set_ylabel(y_label, loc="top", fontweight="bold")

        st.pyplot(fig)
