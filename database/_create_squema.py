import sqlite3
from pathlib import Path

THISDIR = Path(__file__).parent.resolve()
DATABASE = THISDIR/"sessions.db"

def create_schema(database):
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

if __name__ == "__main__":
    if not DATABASE.is_file():
        create_schema(DATABASE)
    else:
        print(f"----"*25)
        print(f"--> Database '{DATABASE}' already exists. <--")
        print(f"----"*25)