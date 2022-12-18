import sqlite3
from itertools import count


SQL_MAKE_TABLE = """CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY,
    time_stamp TEXT NOT NULL,
    player INTEGER NOT NULL,
    test_name TEXT NOT NULL,
    cut_off TEXT NOT NULL,
    stage_of_disease TEXT NOT NULL,
    outcome INTEGER NOT NULL,
    time_to_complete INTEGER NOT NULL,
    num_scans INTEGER NOT NULL
    )"""

_db = sqlite3.connect('scores.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

scores = _db.cursor()
scores.execute(SQL_MAKE_TABLE)

_id = count(start=get_max_id())


def get_max_id():
    try:
        result = scores.execute("SELECT MAX(id) FROM scores")
    except:
        result = 0
    return int(result)


def add_results(*args):
    scores.execute("INSERT INTO scores(?,?,?,?,?,?,?,?,?)", args)
    scores.commit()

