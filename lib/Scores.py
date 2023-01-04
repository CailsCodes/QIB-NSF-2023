import sqlite3

class Scores:

    def __init__(self, fp="scores.db"):
        self.SQL_MAKE_TABLE = """CREATE TABLE IF NOT EXISTS scores (
            time_stamp TEXT NOT NULL,
            time_to_complete INTEGER NOT NULL,
            player INTEGER NOT NULL,
            box1 INTEGER NOT NULL,
            box2 INTEGER NOT NULL,
            box3 INTEGER NOT NULL,
            tests_delivered INTEGER NOT NULL,
            outcome INTEGER NOT NULL
            )"""

        self._db = sqlite3.connect(fp, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.scores = self._db.cursor()
        self.scores.execute(self.SQL_MAKE_TABLE)

    def add_results(self, *args):
        self.scores.execute("INSERT INTO scores VALUES (?,?,?,?,?,?,?,?)", args)
        self._db.commit()

