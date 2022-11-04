from io import BufferedReader
from pathlib import Path
from typing import Union

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
    return f"{'-'.join(toddler.name.split())}_{date}.mp4"


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