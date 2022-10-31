from therapy_aid_tool.DAOs.dao import DAO
from therapy_aid_tool.models.toddler import Toddler


class ToddlerDAO(DAO):
    def __init__(self, database: str) -> None:
        super().__init__(database)

    def _adapt_values(self):
        pass

    def _convert_values(self):
        pass

    def _get_id(self, name) -> int:
        querry = f"SELECT id FROM toddlers WHERE name = {name!r}"
        res = self.cur.execute(querry).fetchone()[0]
        self.con.commit()
        return res

    def add(self, toddler: Toddler):
        querry = "INSERT INTO toddlers(name) VALUES(?)"
        self.cur.execute(querry, [toddler.name])
        self.con.commit()

    def update(self,):
        pass

    def remove(self, name: str):
        querry = f"DELETE FROM toddlers WHERE name = {name!r}"
        self.cur.execute(querry)
        self.con.commit()

    def get(self, name: str):
        querry = f"SELECT name FROM toddlers WHERE name = {name!r}"
        res = self.cur.execute(querry).fetchone()
        if res is None:
            raise Exception(
                f"The name {name!r} was not found in the actors table")
        return Toddler(*res)
