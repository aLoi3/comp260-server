import sqlite3
import hashlib
import cryptography

from cryptography.fernet import Fernet

from colorama import init
from colorama import Fore
init(autoreset=True)


class Input:
    def __init__(self):
        self.current_input = ''
        self.all_connected_clients = ''
        self.current_client = ''

    # Function to check if there are players in the room
    def check_room_for_players(self, my_player):
        clients_in_room = {}
        for client in self.all_connected_clients:
            new_player = self.all_connected_clients.get(client)
            if my_player.current_room is new_player.current_room:
                if client is not self.current_client:
                    clients_in_room[client] = 0

        return clients_in_room

    # Outputs help commands
    def print_help(self):
        return " I will be your guide through this worst-ever-made dungeon... That's what I think, at least. And please, read me as if it was a spooky ghost, deal? BOOooOOoo \n" \
               " Nevertheless, these are your possible commands: \n" \
               " go <direction> \n Directions: NORTH, SOUTH, EAST, WEST \n" \
               " name <your_name>: Change your name to the one you want" \
               " NOTE: If you are not using any of the commands, it will be a normal text and everyone in the room will hear it. \n" \


    def player_input(self, current_input, client, dungeon, database):
        self.current_input = current_input
        self.current_client = client
        self.database = sqlite3.connect(database)
        self.cursor = self.database.cursor()
        self.salt_value = None
        my_dungeon = dungeon
        my_player = self.all_connected_clients.get(client)

        split_input = current_input.split(' ', 1)
        command = split_input[0].lower()
        if len(split_input) >= 2:
            direction = split_input[1].lower()
        else:
            direction = ''

        if command == 'start':
            return my_dungeon.DisplayCurrentRoom(my_player)

        elif command == 'help':
            return Fore.MAGENTA + self.print_help() + Fore.RESET

        # Commands to go to a room
        elif command == 'go':
            if my_dungeon.room[my_player.current_room].HasExit(direction):
                if direction == 'north':
                    self.join_leave_message(my_player, 'left')
                    my_player.current_room = my_dungeon.room[my_player.current_room].north
                    self.join_leave_message(my_player, 'joined')
                    return my_dungeon.DisplayCurrentRoom(my_player)

                if direction == 'east':
                    self.join_leave_message(my_player, 'left')
                    my_player.current_room = my_dungeon.room[my_player.current_room].east
                    self.join_leave_message(my_player, 'joined')
                    return my_dungeon.DisplayCurrentRoom(my_player)

                if direction == 'south':
                    self.join_leave_message(my_player, 'left')
                    my_player.current_room = my_dungeon.room[my_player.current_room].south
                    self.join_leave_message(my_player, 'joined')
                    return my_dungeon.DisplayCurrentRoom(my_player)

                if direction == 'west':
                    self.join_leave_message(my_player, 'left')
                    my_player.current_room = my_dungeon.room[my_player.current_room].west
                    self.join_leave_message(my_player, 'joined')
                    return my_dungeon.DisplayCurrentRoom(my_player)
            else:
                return self.handleBadInput()

        # Change player name
        elif command == "name":
            my_player.player_name = split_input[1]
            return "You are no more a stranger, You named yourself " + split_input[1]

        else:
            # Chat messages
            message = Fore.RED + my_player.player_name + ': ' + Fore.GREEN + ' '.join(split_input)
            self_message = Fore.LIGHTBLUE_EX + 'Your words: ' + Fore.GREEN + ' '.join(split_input)
            client.send(self_message.encode())
            clients_in_room = self.check_room_for_players(my_player)
            for client in clients_in_room:
                client.send(message.encode())
            return

        if command == "register":
            self.register()

        if command == "login":
            self.login()

        if command == "exit":
            self.exit()

    # Message to output whether the player has left or joined the room
    def join_leave_message(self, player, join_or_leave):
        clients_in_the_room = self.check_room_for_players(player)
        message_output = player.player_name + " has " + join_or_leave + " the room..."
        for client in clients_in_the_room:
            client.send(message_output.encode())

    def register(self):
        #cmd = 'CREATE TABLE IF NOT EXISTS users (username varchar(20), password varchar(20) )'
        #self.cursor.execute(cmd)

        username = input("Username: ")
        password = input("Password: ")

        # Put a bit of salt into the password
        salted_password = self.password_salt(password)

        # Now add a spoon of encryption to top it off
        # encrypted_password = self.fernet_crypto(salted_password)

        # Voila - we get extremely uncrackable password... * Just believe *
        try:
            cmd = "SELECT * FROM users WHERE username == '" + username + "'"
            self.cursor.execute(cmd)
            rows = self.cursor.fetchall()

            if len(rows) == 0:
                cmd = 'INSERT INTO users(username, password) values(?,?)'
                self.cursor.execute(cmd, (username, salted_password))
                self.database.commit()

        except Exception:
            print("Failed to Add to Database \n")

    def password_salt(self, password):
        salt = hashlib.md5()
        salt.update(bytes('salty mcsalt-salt', 'utf-8'))

        self.salt_value = salt.hexdigest()

        simple_hash = hashlib.md5()
        simple_hash.update(bytes(password + self.salt_value, 'utf-8'))

        salted_password = simple_hash.hexdigest()

        return salted_password

    def fernet_crypto(self, password):
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        cipher_text = cipher_suite.encrypt(bytes(password.encode('utf-8')))
        #plain_text = cipher_suite.decrypt(cipher_text)     # get decrypted password (salted at the time)

        return cipher_text

    def login(self):
        username = input("Username: ")
        password = input("Password: ")

        hash_check = hashlib.md5()
        hash_check.update(bytes(password + self.salt_value, 'utf-8'))

        password = hash_check.hexdigest()

        try:
            cmd = "SELECT username, password FROM users WHERE username = ? AND password = ?"
            self.cursor.execute(cmd, (username, password))
            rows = self.cursor.fetchall()
            for row in rows:
                username_check = '{0}'.format(row[0])
                password_check = '{0}'.format(row[1])

                if(username == username_check and password == password_check):
                    # ToDo: Do Login Here
                    print("Login here")
                else:
                    print("Username or Password are incorrect")

        except Exception:
            print("Failed to Login")

    def exit(self):
        # ToDo: Implement exit here
        print("Cause errors... And Python")

    # Message to output if the player chooses unavailable direction to go
    def handleBadInput(self):
        return "Bad Input \n"
