from abc import ABC, abstractmethod

import sqlite3


class DAO(ABC):
    @abstractmethod
    def __init__(self, database) -> None:
        self.__db = database
        self.con, self.cur = self.__establish_connection()

    def __establish_connection(self):
        con = sqlite3.connect(self.__db)
        cur = con.cursor()
        # Allow foreign keys
        cur.execute("PRAGMA foreign_keys = ON")
        return con, cur

    @abstractmethod
    def _adapt_values(self):
        """Adapt non-SQL compliant Python objects to be stored as SQL JSON formatted string"""
        pass

    @abstractmethod
    def _convert_values(self):
        """Recreate SQL JSON formatted string to Python object"""
        pass

    @abstractmethod
    def _get_id(self):
        pass

    @abstractmethod
    def _get_from_id(self, id):
        pass

    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def remove(self):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def get_all(self):
        pass
