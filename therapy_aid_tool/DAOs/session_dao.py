from therapy_aid_tool.DAOs.dao import DAO
from therapy_aid_tool.DAOs.toddler_dao import ToddlerDAO
from therapy_aid_tool.DAOs.video_dao import VideoDAO

from therapy_aid_tool.models.session import Session
from therapy_aid_tool.models.toddler import Toddler
from therapy_aid_tool.models.video import Video

import json


class SessionDAO(DAO):
    def __init__(self, database: str) -> None:
        super().__init__(database)
        self.__toddler_dao = ToddlerDAO(database)
        self.__video_dao = VideoDAO(database)

    def add(self, session: Session):
        querry = """
            INSERT INTO sessions(toddler_id, video_id, date) 
            VALUES(?, ?, ?)"""
        toddler_id = self.__toddler_dao._get_id(session.toddler.name)
        video_id = self.__video_dao._get_id(session.video.filepath)
        self.cur.execute(querry, [toddler_id, video_id, session.date])
        self.con.commit()

    def _adapt_values(self, session: Session):
        pass

    def _convert_values(self, values_fetched):
        pass

    def _get_id(self):
        pass

    def update(self,):
        pass

    def remove(self, name: str):
        pass

    def get(self, toddler: Toddler, date: str):
        pass

    def get_all(self):
        querry = f"SELECT * FROM sessions"
        res = self.cur.execute(querry).fetchall()
        return res
