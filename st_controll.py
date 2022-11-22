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


ROOT = Path(__file__).parents[0].resolve()

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
