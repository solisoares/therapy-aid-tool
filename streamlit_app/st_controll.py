import streamlit as st

from copy import deepcopy
from io import BufferedReader
from pathlib import Path
from typing import Union

import numpy as np
import matplotlib.pyplot as plt

from therapy_aid_tool.models.toddler import Toddler
from therapy_aid_tool.models.video import Video
from therapy_aid_tool.models.session import Session

from therapy_aid_tool.DAOs.toddler_dao import ToddlerDAO
from therapy_aid_tool.DAOs.video_dao import VideoDAO
from therapy_aid_tool.DAOs.session_dao import SessionDAO


ROOT = Path(__file__).parents[1].resolve()

DATABASE_DIR = ROOT/"database"
DATABASE = DATABASE_DIR/"sessions.db"

VIDEOS_DIR = DATABASE_DIR/"videos"


def save_user_video(video: BufferedReader, location: Union[str, Path]):
    """Save the user uploaded video

    The type of the streamlit uploaded video is a "UploadedFile" but respects
    the Buffer protocol

    Args:
        video (BufferedReader): The user uploaded video to the streamlit app
        location (Union[str, Path]): Where to save this video
    """
    with open(location, "wb") as f:
        f.write(video.read())


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
    return ToddlerDAO(DATABASE).get_all_names()


def dates_from_name(name: str):
    return SessionDAO(DATABASE).get_dates_from_name(name)


def get_session(toddler_name: str, date: str):
    return SessionDAO(DATABASE).get(toddler_name, date)


def __sessions_from_name(toddler_name: str):
    """Get all the sessions that a toddler is present

    Args:
        toddler_name (str): The name o the toddler   
    """
    return SessionDAO(DATABASE).get_all_from_name(toddler_name)


def __statistics_from_all_sessions(toddler_name: str):
    sessions = __sessions_from_name(toddler_name)
    # interactions for each video
    _statistics = [session.video.interactions_statistics
                               for session in sessions]
    # Merge these interactions
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
    for _dict in _statistics:
        for _k, _v in _dict.items():
            for __k, __v in _v.items():
                statistics[_k][__k].append(__v)
    return statistics


def plot_sessions_progress(toddler_name: str):
    """Plots the progress of a toddler over the sessions they appear

    Args:
        toddler_name (str): The name o the toddler
    """
    statistics = __statistics_from_all_sessions(toddler_name)

    titles = {
        'td_ct': 'Toddler-Caretaker',
        'td_pm': 'Toddler-PlusMe',
        'ct_pm': 'Caretaker-PlusMe',
    }

    colors = {
        'n_interactions': 'blue',
        'total_time': 'red',
        'min_time': 'green',
        'max_time': 'yellow',
        'mean_time': 'black',
    }

    labels = {
        'n_interactions': 'nº interactions',
        'total_time': 'total time (s)',
        'min_time': 'min time (s)',
        'max_time': 'max time (s)',
        'mean_time': 'mean time (s)',
    }
    n_sessions = len(statistics['td_ct']['n_interactions'])
    x = np.arange(1, n_sessions + 1)
    for type, statistic in statistics.items():
        fig, ax = plt.subplots()
        for k, v in statistic.items():
            ax.plot(x, v, 'bo-', alpha=0.8, color=colors[k], label=labels[k])
            ax.legend()
            ax.set_title(titles[type])
            ax.grid()
            ax.set_xlabel("sessions", loc="right")
        st.pyplot(fig)
