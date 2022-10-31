from therapy_aid_tool.DAOs.dao import DAO
from therapy_aid_tool.models.video import Video
import json


class VideoDAO(DAO):
    def __init__(self, database: str) -> None:
        super().__init__(database)

    def add(self, video: Video):
        querry = """
            INSERT INTO 
            videos(filepath, closeness, interactions, interactions_statistics) 
            VALUES(?, ?, ?, ?)"""
        self.cur.execute(querry, [*self._adapt_values(video)])
        self.con.commit()

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

    def _get_id(self, filepath) -> int:
        querry = f"SELECT id FROM videos WHERE filepath = '{filepath}'"
        res = self.cur.execute(querry).fetchone()[0]
        self.con.commit()
        return res

    def update(self,):
        pass

    def remove(self, name: str):
        querry = f"DELETE FROM videos WHERE name = {name!r}"
        self.cur.execute(querry)
        self.con.commit()

    def get(self, filepath: str):
        querry = f"""SELECT filepath, closeness, interactions, interactions_statistics
                     FROM videos WHERE filepath = '{filepath}'"""
        res = self._convert_values(self.cur.execute(querry).fetchone())
        if res is None:
            raise Exception(
                f"The filepath '{filepath}' was not found in the actors table")
        return Video(*res)

    def get_all(self):
        querry = f"SELECT * FROM videos"
        res = self.cur.execute(querry).fetchall()
        return res
