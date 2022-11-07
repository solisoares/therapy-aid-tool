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

    def _adapt_values(self, session: Session):
        toddler_id = self.__toddler_dao._get_id(session.toddler.name)
        video_id = self.__video_dao._get_id(session.video.filepath)
        date = session.date
        return toddler_id, video_id, date

    def _convert_values(self, values_fetched):
        toddler_id, video_id, date = values_fetched
        toddler = self.__toddler_dao._get_from_id(toddler_id)
        video = self.__video_dao._get_from_id(video_id)
        return toddler, video, date

    def _get_id(self, toddler_name: str, date: str):
        toddler_id = self.__toddler_dao._get_id(toddler_name)
        if not toddler_id:
            return
        querry = f"SELECT id FROM sessions WHERE toddler_id = {toddler_id} AND date = '{date}'"
        res = self.cur.execute(querry).fetchone()
        if res:
            self.con.commit()
            return res[0]

    def _get_from_id(self, id):
        pass

    def add(self, session: Session):
        if not self._get_id(session.toddler.name, session.date):
            querry = """
                INSERT INTO sessions(toddler_id, video_id, date) 
                VALUES(?, ?, ?)"""
            toddler_id = self.__toddler_dao._get_id(session.toddler.name)
            video_id = self.__video_dao._get_id(session.video.filepath)
            self.cur.execute(querry, [toddler_id, video_id, session.date])
            self.con.commit()

    def update(self, toddler_name: str, date: str, new_session: Session):
        id = self._get_id(toddler_name, date)
        if id and not self._get_id(new_session.toddler.name, new_session.date):
            querry = f"""
                UPDATE sessions
                SET toddler_id = ?, video_id = ?, date = ?
                WHERE id = ?;
                """
            new_values = self._adapt_values(new_session)
            self.cur.execute(querry, [*new_values, id])
            self.con.commit()

    def remove(self, toddler_name: str, date: str):
        toddler_id = self.__toddler_dao._get_id(toddler_name)
        if not toddler_id:
            return
        querry = f"DELETE FROM sessions WHERE toddler_id = {toddler_id} AND date = {date!r}"
        self.cur.execute(querry)
        self.con.commit()

    def get(self, toddler_name: str, date: str):
        toddler_id = self.__toddler_dao._get_id(toddler_name)
        if not toddler_id:
            return
        querry = f"""SELECT toddler_id, video_id, date
                     FROM sessions WHERE toddler_id = {toddler_id} AND date = '{date}'"""
        res = self.cur.execute(querry).fetchone()
        if res is None:
            return
        res = self._convert_values(res)
        return Session(*res)

    def get_all(self):
        querry = f"SELECT * FROM sessions"
        res = self.cur.execute(querry).fetchall()
        return res

    def get_all_from_name(self, toddler_name: str):
        toddler_id = self.__toddler_dao._get_id(toddler_name)
        querry = f"SELECT toddler_id, video_id, date FROM sessions WHERE toddler_id = ?"
        res = self.cur.execute(querry, [toddler_id]).fetchall()
        res = [Session(*self._convert_values(item)) for item in res if res]
        return res

    def get_all_dates(self):
        querry = f"SELECT date FROM sessions"
        res = self.cur.execute(querry).fetchall()
        res = [item[0] for item in res if res]
        return res

    def get_dates_from_name(self, toddler_name: str):
        toddler_id = self.__toddler_dao._get_id(toddler_name)
        querry = f"SELECT date FROM sessions WHERE toddler_id = ?"
        res = self.cur.execute(querry, [toddler_id]).fetchall()
        res = [item[0] for item in res if res]
        return res
