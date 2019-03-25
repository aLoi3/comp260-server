import sqlite3


class Database:
    def __init__(self):
        self.isRunning = True
        self.database = None
        self.cursor = None

    def create_database(self):
        try:
            self.database = sqlite3.connect('dataTest.sql')
            self.cursor = self.database.cursor()
            self.cursor.execute('CREATE TABLE table_phonenumbers (name varchar(20), number varchar(20) ) ')
        except:
            print('Failed to create Database \n')

    def add_data(self):
        name = input('Name ')
        number = input('Number ')

        try:
            self.cursor.execute("SELECT * FROM table_phonenumbers WHERE name == '" + name + "'")
            rows = self.cursor.fetchall()

            if len(rows) == 0:
                self.cursor.execute('insert into table_phonenumbers(name, number) values(?,?)', (name, number))
                self.database.commit()

        except:
            print('Failed to add to Database \n')

    def display_database(self):
        try:
            rows = self.cursor.execute("SELECT * FROM " + "table_phonenumbers" + " order by name asc")

            for row in rows:
                print(row[0] + ' ' + row[1] + '\n')

        except:
            print('Failed to display Database \n')

    def exit_application(self):
        self.isRunning = False

    def run(self):
        while self.isRunning is True:
            print('Type 1 to Create Database')
            print('Type 2 to Add your name and number to Database')
            print('Type 3 to Display everything')
            print('Type x to exit the application \n')

            key = input("> ")

            if key is '1':
                self.create_database()

            if key is '2':
                self.add_data()

            if key is '3':
                self.display_database()

            if key is 'x':
                self.exit_application()


if __name__ == '__main__':
    database = Database()
    database.run()
