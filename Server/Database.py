import sqlite3


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

    def add_player(self, username, room, player_name):
        cmd = '''INSERT INTO players (owner_username, current_room, player_name) values(?,?,?)'''
        self.cursor.execute(cmd, (username, room, player_name))
        self.database.commit()
        print("Successfully added player")

    def get_value(self, field_to_check, table, query_field, query_value):
        cmd = "SELECT " + field_to_check + " FROM " + table + " WHERE " + query_field + " =?"
        self.cursor.execute(cmd, (query_value, ))
        result = self.cursor.fetchone()
        return result[0]

    def get_all_values(self, field_to_check, table, query_field, query_value):
        cmd = "SELECT " + field_to_check + " FROM " + table + " WHERE " + query_field + " =?"
        self.cursor.execute(cmd, (query_value, ))
        result = self.cursor.fetchall()
        return result

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

    def get_current_room(self, player):
        cmd = "SELECT current_room FROM players WHERE player_name =?"
        self.cursor.execute(cmd, (player, ))
        result = self.cursor.fetchone()
        return result[0]

    def set_current_room(self, player, room):
        cmd = "UPDATE players SET current_room =? WHERE player_name =?"
        self.cursor.execute(cmd, (room, player))
        self.database.commit()

    def set_stat_value(self, stat, player, amount):
        cmd = "UPDATE players SET " + stat + " =? WHERE player_name =?"
        self.cursor.execute(cmd, (amount, player))
        self.database.commit()

    def get_connection(self, direction, current_room):
        cmd = "SELECT " + direction + " FROM dungeon WHERE name =?"
        self.cursor.execute(cmd, (current_room, ))
        result = self.cursor.fetchone()
        return result[0]

    def create_player_database(self):
        try:
            cmd = '''CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY, 
            owner_username TEXT, 
            current_room TEXT, 
            player_name TEXT, 
            player_class TEXT, 
            experience INTEGER DEFAULT 0, 
            strength INTEGER DEFAULT 0, 
            agility INTEGER DEFAULT 0, 
            intelligence INTEGER DEFAULT 0, 
            hearing INTEGER DEFAULT 0, 
            observation INTEGER DEFAULT 0 
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
            north TEXT DEFAULT '', 
            east TEXT DEFAULT '', 
            south TEXT DEFAULT '', 
            west TEXT DEFAULT '', 
            up TEXT DEFAULT '', 
            down TEXT DEFAULT ''
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
