import sqlite3
from itertools import count

class Scores:

    def __init__(self, fp="scores.db"):
        self.SQL_MAKE_TABLE = """CREATE TABLE IF NOT EXISTS scores (
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

        self._db = sqlite3.connect(fp, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.scores = self._db.cursor()
        self.scores.execute(self.SQL_MAKE_TABLE)
        self._id = count(start=self.get_max_id())


    def get_max_id(self):
        try:
            result = self.scores.execute("SELECT MAX(id) FROM scores")
        except:
            result = 0
        return int(result)


    def add_results(self, *args):
        self.scores.execute("INSERT INTO scores(?,?,?,?,?,?,?,?,?)", args)
        self.scores.commit()

