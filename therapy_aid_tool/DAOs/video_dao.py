from therapy_aid_tool.DAOs.dao import DAO
from therapy_aid_tool.models.video import Video
import json


class VideoDAO(DAO):
    def __init__(self, database: str) -> None:
        super().__init__(database)

    def _adapt_values(self, video: Video):
        filepath = video.filepath
        closeness = json.dumps(video.closeness)
        interactions = json.dumps(video.interactions)
        interactions_statistics = json.dumps(video.interactions_statistics)
        return filepath, closeness, interactions, interactions_statistics

    def _convert_values(self, values_fetched):
        (filepath, _closeness,
         _interactions, _interactions_statistics) = values_fetched
        closeness = json.loads(_closeness)
        interactions = json.loads(_interactions)
        interactions_statistics = json.loads(_interactions_statistics)
        return filepath, closeness, interactions, interactions_statistics

    def _get_id(self, filepath):
        querry = f"SELECT id FROM videos WHERE filepath = '{filepath}'"
        res = self.cur.execute(querry).fetchone()
        if res:
            self.con.commit()
            return res[0]

    def _get_from_id(self, id):
        querry = f"""SELECT filepath, closeness, interactions, interactions_statistics
                     FROM videos WHERE id = {id}"""
        res = self.cur.execute(querry).fetchone()
        if res is None:
            return
        res = self._convert_values(res)
        return Video(*res)

    def add(self, video: Video):
        if not self._get_id(video.filepath):
            querry = """
                INSERT INTO 
                videos(filepath, closeness, interactions, interactions_statistics) 
                VALUES(?, ?, ?, ?)"""
            self.cur.execute(querry, [*self._adapt_values(video)])
            self.con.commit()

    def update(self, filepath, new_video: Video):
        if self._get_id(filepath) and not self._get_id(new_video.filepath):
            querry = f"""
                UPDATE videos
                SET filepath = ?, closeness = ?, interactions = ?, interactions_statistics = ?
                WHERE filepath = ?;
                """
            new_values = self._adapt_values(new_video)
            self.cur.execute(querry,[*new_values, filepath])
            self.con.commit()

    def remove(self, filepath: str):
        querry = f"DELETE FROM videos WHERE filepath = '{filepath}'"
        self.cur.execute(querry)
        self.con.commit()

    def get(self, filepath: str):
        querry = f"""SELECT filepath, closeness, interactions, interactions_statistics
                     FROM videos WHERE filepath = '{filepath}'"""
        res = self.cur.execute(querry).fetchone()
        if res is None:
            return
            # raise Exception(
            #     f"The filepath '{filepath}' was not found in the actors table")
        res = self._convert_values(res)
        return Video(*res)

    def get_all(self):
        querry = f"SELECT * FROM videos"
        res = self.cur.execute(querry).fetchall()
        return res
