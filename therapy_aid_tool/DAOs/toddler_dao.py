from therapy_aid_tool.DAOs.dao import DAO
from therapy_aid_tool.models.toddler import Toddler


class ToddlerDAO(DAO):
    def __init__(self, database: str) -> None:
        super().__init__(database)

    def _adapt_values(self):
        pass

    def _convert_values(self):
        pass

    def _get_id(self, name):
        querry = f"SELECT id FROM toddlers WHERE name = {name!r}"
        res = self.cur.execute(querry).fetchone()
        if res:
            self.con.commit()
            return res[0]

    def _get_from_id(self, id):
        querry = f"SELECT name FROM toddlers WHERE id = {id}"
        res = self.cur.execute(querry).fetchone()
        if res is None:
            return 
        return Toddler(*res)

    def add(self, toddler: Toddler):
        if not self._get_id(toddler.name):
            querry = "INSERT INTO toddlers(name) VALUES(?)"
            self.cur.execute(querry, [toddler.name])
            self.con.commit()

    def update(self, name, new_toddler: Toddler):
        if self._get_id(name) and not self._get_id(new_toddler.name):
            querry = f"""
                UPDATE toddlers
                SET name = ?
                WHERE name = ?;
                """
            self.cur.execute(querry, [new_toddler.name, name])
            self.con.commit()

    def remove(self, name: str):
        querry = f"DELETE FROM toddlers WHERE name = {name!r}"
        self.cur.execute(querry)
        self.con.commit()

    def get(self, name: str):
        querry = f"SELECT name FROM toddlers WHERE name = {name!r}"
        res = self.cur.execute(querry).fetchone()
        if res is None:
            return 
            # raise Exception(
            #     f"The name {name!r} was not found in the actors table")
        return Toddler(*res)

    def get_all(self):
        querry = f"SELECT * FROM toddlers"
        res = self.cur.execute(querry).fetchall()
        return res

    def get_all_names(self):
        querry = f"SELECT name FROM toddlers"
        res = self.cur.execute(querry).fetchall()
        res = [item[0] for item in res if res]
        return res