from therapy_aid_tool.models.toddler import Toddler
from therapy_aid_tool.models.video import Video


class Session:
    def __init__(self, toddler: Toddler, video: Video, date: str) -> None:
        self.__toddler = toddler
        self.__video = video
        self.__date = date

    def __repr__(self):
        return f"Session(toddler={self.__toddler}, video='{self.__video}', date='{self.__date}')"

    # Getters
    @property
    def toddler(self):
        return self.__toddler

    @property
    def video(self):
        return self.__video

    @property
    def date(self):
        return self.__date

    # Setters
    @toddler.setter
    def toddler(self, toddler):
        self.__toddler = toddler

    @video.setter
    def video(self, video):
        self.__video = video

    @date.setter
    def date(self, date):
        self.__date = date
