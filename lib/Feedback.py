import sqlite3

class Feedback:

    def __init__(self, fp="feedback.db"):
        self.SQL_MAKE_TABLE = """CREATE TABLE IF NOT EXISTS feedback (
            time_stamp TEXT NOT NULL,
            player INTEGER NOT NULL,
            question INTEGER NOT NULL,
            answer INTEGER NOT NULL
            )"""
        
        self._db = sqlite3.connect(fp, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.feedback = self._db.cursor()
        self.feedback.execute(self.SQL_MAKE_TABLE)

    def add_feedback(self, *args):
        self.feedback.execute("INSERT INTO feedback VALUES (?,?,?,?)", args)
        self._db.commit()