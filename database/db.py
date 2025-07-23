from database import queries
import sqlite3

DB_NAME = "konkurs.db"


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()

    def execute(self, query, params: tuple = ()):
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetchone(self, query, params: tuple = ()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetchall(self, query, params: tuple = ()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()


def setup_database():
    db = Database()
    db.execute(queries.CREATE_USERS_TABLE)
    db.close()


# Global `db` object
db = Database()
