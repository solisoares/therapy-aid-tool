import sqlite3
from pathlib import Path


def _create_schema(database):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON")

    # Toddlers Table
    querry = "CREATE TABLE toddlers(id INTEGER PRIMARY KEY, name TEXT);"
    cur.execute(querry)
    con.commit()

    # Videos Table
    querry = """CREATE TABLE videos(
        id INTEGER PRIMARY KEY,
        filepath TEXT,
        closeness TEXT,
        interactions TEXT,
        interactions_statistics TEXT);"""
    cur.execute(querry)
    con.commit()

    # Sessions Table
    querry = """CREATE TABLE sessions(
        id INTEGER PRIMARY KEY,
        toddler_id,
        video_id,
        date TEXT,
        FOREIGN KEY(toddler_id) REFERENCES toddlers(id),
        FOREIGN KEY(video_id) REFERENCES videos(id)
        );"""
    cur.execute(querry)
    con.commit()


def create_schema(database):
    database = Path(database)
    if not database.is_file():
        with open(database, "wb"):  # create db file
            pass
        _create_schema(database)


if __name__ == "__main__":
    ROOT = Path(__file__).parents[2].resolve()
    DATABASE = ROOT/"database/sessions.db"
    if DATABASE.is_file():
        print(
            f"\n{'----'*25}\n--> Database '{DATABASE}' already exists. <--\n{'----'*25}\n")
    else:
        create_schema(DATABASE)
