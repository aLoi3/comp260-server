import sqlite3
import hashlib


class Database:
    def __init__(self):
        self.isRunning = True
        self.database = None
        self.cursor = None

    def create_database(self):
        try:
            self.database = sqlite3.connect('dataTest.sql')
            self.cursor = self.database.cursor()
            cmd = 'CREATE TABLE users (username varchar(20), password varchar(20) ) '
            self.cursor.execute(cmd)
        except:
            print('Failed to create Database \n')

    def add_data(self):
        username = input('Username: ')
        password = input('Password: ')

        simple_hash = hashlib.md5()
        simple_hash.update(bytes(password, 'utf-8'))
        print("Simple password hash: " + simple_hash.hexdigest())

        salt = hashlib.md5()
        salt.update(bytes('salty mcsalt-salt', 'utf-8'))
        print("Salt: " + salt.hexdigest())

        s = hashlib.md5()
        s.update(bytes(password, 'utf-8') + salt.digest())
        print("Salted password hash: " + s.hexdigest())

        try:
            self.cursor.execute("SELECT * FROM users WHERE username == '" + username + "'")
            rows = self.cursor.fetchall()

            if len(rows) == 0:
                cmd = 'INSERT INTO users(username, password) values(?,?)'
                self.cursor.execute(cmd, (username, s.hexdigest()))
                self.database.commit()

        except:
            print('Failed to add to Database \n')

    def display_database(self):
        try:
            cmd = "SELECT * FROM " + "users" + " order by username asc"
            rows = self.cursor.execute(cmd)

            for row in rows:
                print(row[0] + ' ' + row[1] + '\n')

        except:
            print('Failed to display Database \n')

    def find_contact(self):
        user_name_to_find = input('Username to find: ')

        try:
            cmd = '''SELECT username, password FROM users WHERE username =?'''
            self.cursor.execute(cmd, (user_name_to_find, ))
            rows = self.cursor.fetchall()
            for row in rows:
                print('{0} : {1}'.format(row[0], row[1]))

        except:
            print('Failed to find username')

    def delete_contact(self):
        delete_user = input('Username to delete: ')

        try:
            cmd = '''DELETE FROM users WHERE username = ?'''
            self.cursor.execute(cmd, (delete_user, ))
            self.database.commit()

        except:
            print('Failed to delete the user')

    def exit_application(self):
        self.isRunning = False

    def run(self):
        while self.isRunning is True:
            print('Type 1 to Create Database')
            print('Type 2 to Add your Data')
            print('Type 3 to Display everything')
            print('Type 4 to Find User')
            print('Type 5 to Delete the user')
            print('Type x to exit the application \n')

            key = input("> ")

            if key is '1':
                self.create_database()

            if key is '2':
                self.add_data()

            if key is '3':
                self.display_database()

            if key is '4':
                self.find_contact()

            if key is '5':
                self.delete_contact()

            if key is 'x':
                self.exit_application()


if __name__ == '__main__':
    database = Database()
    database.run()
