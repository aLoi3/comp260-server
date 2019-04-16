import sqlite3
import hashlib
import cryptography
import Database

from cryptography.fernet import Fernet


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
        self.my_database = database
        my_dungeon = dungeon
        my_player = self.all_connected_clients.get(client)

        split_input = current_input.split()
        command = split_input[0].lower()
        if len(split_input) >= 2:
            direction = split_input[1].lower()
        else:
            direction = ''

        if command == 'start':
            return my_dungeon.DisplayCurrentRoom(my_player)

        elif command == 'help':
            return self.print_help()

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

                if direction == 'up':
                    self.join_leave_message(my_player, 'left')
                    my_player.current_room = my_dungeon.room[my_player.current_room].up
                    self.join_leave_message(my_player, 'joined')
                    return my_dungeon.DisplayCurrentRoom(my_player)

                if direction == 'down':
                    self.join_leave_message(my_player, 'left')
                    my_player.current_room = my_dungeon.room[my_player.current_room].down
                    self.join_leave_message(my_player, 'joined')
                    return my_dungeon.DisplayCurrentRoom(my_player)
            else:
                return self.handleBadInput()

        elif command == "register":
            #self.register()

            username = split_input[1]
            password = split_input[2]

            salt = hashlib.md5()
            salt.update(bytes('salty mcsalt-salt', 'utf-8'))

            salt_value = salt.hexdigest()

            simple_hash = hashlib.md5()
            simple_hash.update(bytes(password + salt_value, 'utf-8'))

            salted_password = simple_hash.hexdigest()

            self.my_database.add_user(username, salted_password, salt_value)

        elif command == "login":
            #self.login()

            username = split_input[1]
            password = split_input[2]

            salt = self.my_database.get_value("salt", "users", "username", username)

            simple_hash = hashlib.md5()
            simple_hash.update(bytes(password + salt, 'utf-8'))
            salted_password = simple_hash.hexdigest()

            if (self.my_database.check_value("username", "users", "username", username, username) is True):
                if (self.my_database.check_value("password", "users", "username", username, salted_password) is True):
                    # TO:DO Change the state to logged in state
                    print("Successfully logged in")
                else:
                    print("Password is incorrect")
            else:
                print("Username is incorrect")


        # Change player name
        elif command == "name":
            my_player.player_name = split_input[1]
            return "You are no more a stranger, You named yourself " + split_input[1]

        else:
            # Chat messages
            message = my_player.player_name + ': ' + ' '.join(split_input)
            self_message = 'Your words: ' + ' '.join(split_input)
            client.send(self_message.encode())
            clients_in_room = self.check_room_for_players(my_player)
            for client in clients_in_room:
                client.send(message.encode())
            return

        if command == "exit":
            self.exit()

    # Message to output whether the player has left or joined the room
    def join_leave_message(self, player, join_or_leave):
        clients_in_the_room = self.check_room_for_players(player)
        message_output = player.player_name + " has " + join_or_leave + " the room..."
        for client in clients_in_the_room:
            client.send(message_output.encode())

    def register(self):
        username = input("Username: ")
        password = input("Password: ")

        salt = hashlib.md5()
        salt.update(bytes('salty mcsalt-salt', 'utf-8'))

        salt_value = salt.hexdigest()

        simple_hash = hashlib.md5()
        simple_hash.update(bytes(password + salt_value, 'utf-8'))

        salted_password = simple_hash.hexdigest()

        self.my_database.add_user(username, salted_password, salt_value)

    def fernet_crypto(self, password):
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        cipher_text = cipher_suite.encrypt(bytes(password.encode('utf-8')))
        #plain_text = cipher_suite.decrypt(cipher_text)     # get decrypted password (salted at the time)

        return cipher_text

    def login(self):
        username = input("Username: ")
        password = input("Password: ")

        salt = self.my_database.get_value("salt", "users", "username", username)

        simple_hash = hashlib.md5()
        simple_hash.update(bytes(password + salt, 'utf-8'))
        salted_password = simple_hash.hexdigest()

        if(self.my_database.check_value("username", "users", "username", username, username) is True):
            if(self.my_database.check_value("password", "users", "username", username, salted_password) is True):
                # TO:DO Change the state to logged in state
                print("Successfully logged in")

    def exit(self):
        # ToDo: Implement exit here
        print("Cause errors... And Python")

    # Message to output if the player chooses unavailable direction to go
    def handleBadInput(self):
        return "Bad Input \n"
