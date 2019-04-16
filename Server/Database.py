import sqlite3
import hashlib


class Database:
    def __init__(self):
        self.database = sqlite3.connect("Database.sql")
        self.cursor = self.database.cursor()

        self.create_player_database()
        self.create_dungeon_database()
        self.create_user_database()

    def add_user(self, username, password, salt):
        cmd = '''INSERT INTO users (username, password, salt) values(?,?,?)'''
        self.cursor.execute(cmd, (username, password, salt))
        self.database.commit()
        print("Successfully added user")

    def add_player(self, username, player_name):
        cmd = '''INSERT INTO players (owner_username, player_name) values(?,?)'''
        self.cursor.execute(cmd, (username, player_name))
        self.database.commit()
        print("Successfully added player")

    def get_value(self, field_to_check, table, query_field, query_value):
        cmd = "SELECT " + field_to_check + " FROM " + table + " WHERE " + query_field + " =?"
        self.cursor.execute(cmd, (query_value, ))
        result = self.cursor.fetchone()
        return result[0]

    def check_value(self, field_to_check, table, query_field, query_value, value_to_check):
        cmd = "SELECT " + field_to_check + " FROM " + table + " WHERE " + query_field + " =?"
        self.cursor.execute(cmd, (query_value, ))
        result = self.cursor.fetchone()
        if result is not None:
            if result[0] == value_to_check:
                return True
            else:
                return False
        else:
            return False

    def create_player_database(self):
        try:
            cmd = '''CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY, 
            owner_username TEXT, 
            current_room INTEGER DEFAULT 1, 
            player_name TEXT 
            )'''
            self.cursor.execute(cmd)
            self.database.commit()

            print("Player table created...")
        except Exception:
            print("Failed to Create Database \n")

    def create_dungeon_database(self):
        try:
            cmd = '''CREATE TABLE IF NOT EXISTS dungeon (
            name TEXT PRIMARY KEY, 
            description TEXT, 
            north INTEGER DEFAULT '', 
            east INTEGER DEFAULT '', 
            south INTEGER DEFAULT '', 
            west INTEGER DEFAULT '', 
            up INTEGER DEFAULT '', 
            down INTEGER DEFAULT ''
            )'''
            self.cursor.execute(cmd)
            self.database.commit()

            print("Dungeon table created...")
        except Exception:
            print("Failed to Create Database \n")

    def create_user_database(self):
        try:
            cmd = '''CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY, 
            password TEXT,
            salt TEXT 
            )'''
            self.cursor.execute(cmd)
            self.database.commit()

            print("User table created...")
        except Exception:
            print("Failed to Create Database \n")
