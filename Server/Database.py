import sqlite3
import hashlib


class Database:
    def __init__(self):
        self.database = sqlite3.connect("Database.sql")
        self.cursor = self.database.cursor()

    def create_database(self):
        try:
            cmd = '''CREATE TABLE IF NOT EXISTS users (username varchar(20), password varchar(20) )'''
            self.cursor.execute(cmd)
        except Exception:
            print("Failed to Create Database \n")
