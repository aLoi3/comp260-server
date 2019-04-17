import sqlite3
import hashlib
import cryptography

from cryptography.fernet import Fernet

Idle = 0
In_register = 1
In_Login = 2
Logged_in = 3
In_game = 4


class Input:
    def __init__(self):
        self.all_connected_clients = ''
        self.current_client = ''
        self.current_state = Idle

    # Function to check if there are players in the room
    def check_room_for_players(self, my_player):
        clients_in_room = {}
        for client in self.all_connected_clients:
            new_player = self.all_connected_clients.get(client)
            if my_player.current_room is new_player.current_room:
                if client is not self.current_client:
                    clients_in_room[client] = 0

        return clients_in_room

    def change_state(self, state):
        self.current_state = state

    # Outputs help commands
    def print_help(self):
        return " I will be your guide through this worst-ever-made dungeon... That's what I think, at least. And please, read me as if it was a spooky ghost, deal? BOOooOOoo \n" \
               " Nevertheless, these are your possible commands: \n" \
               " go <direction> \n Directions: NORTH, SOUTH, EAST, WEST \n" \
               " name <your_name>: Change your name to the one you want" \
               " NOTE: If you are not using any of the commands, it will be a normal text and everyone in the room will hear it. \n" \


    def player_input(self, current_input, client, dungeon, database):
        self.current_client = client
        self.my_database = database
        self.my_dungeon = dungeon
        self.my_player = self.all_connected_clients.get(client)

        self.split_input = current_input.split()
        self.command = self.split_input[0].lower()

        print(self.current_state)

        if self.current_state == Idle:
            if self.command == "register":
                message = self.register()
            elif self.command == "login":
                message = self.login()
            else:
                message = "Incorrect Input"

            return message

        elif self.current_state == In_register:
            # To:Do Allow only register here
            print("In register lobby")
            message = self.in_register()

            return message

        elif self.current_state == In_Login:
            print("In login lobby")

            message = self.in_login()

            return message

        elif self.current_state == Logged_in:
            # To:Do: Allow only character chose here
            print("In character lobby")

            if self.command == "start":
                message = self.start()
            else:
                message = "Incorrect Input"

            return message

        elif self.current_state == In_game:
            if self.command == "go":
                message = self.move()
            elif self.command == "help":
                message = self.help()
            elif self.command == "name":
                message = self.change_name()
            else:
                message = "Incorrect Input"

            return message

        elif self.command == "exit":
            self.exit()

        else:
            print("Incorrect command")

    # Message to output whether the player has left or joined the room
    def join_leave_message(self, player, join_or_leave):
        clients_in_the_room = self.check_room_for_players(player)
        message_output = player.player_name + " has " + join_or_leave + " the room..."
        for client in clients_in_the_room:
            client.send(message_output.encode())

    def change_name(self):
        self.my_player.player_name = self.split_input[1]
        return "You are no more a stranger, You named yourself " + self.split_input[1]

    def message(self):
        # Chat messages
        message = self.my_player.player_name + ': ' + ' '.join(self.split_input)
        self_message = 'Your words: ' + ' '.join(self.split_input)
        self.current_client.send(self_message.encode())
        clients_in_room = self.check_room_for_players(self.my_player)
        for client in clients_in_room:
            client.send(message.encode())
        return

    def help(self):
        return self.print_help()

    def move(self):
        if len(self.split_input) >= 2:
            direction = self.split_input[1].lower()
        else:
            direction = ''

        if self.my_dungeon.room[self.my_player.current_room].HasExit(direction):
            if direction == 'north':
                self.join_leave_message(self.my_player, 'left')
                self.my_player.current_room = self.my_dungeon.room[self.my_player.current_room].north
                self.join_leave_message(self.my_player, 'joined')
                return self.my_dungeon.DisplayCurrentRoom(self.my_player)

            if direction == 'east':
                self.join_leave_message(self.my_player, 'left')
                self.my_player.current_room = self.my_dungeon.room[self.my_player.current_room].east
                self.join_leave_message(self.my_player, 'joined')
                return self.my_dungeon.DisplayCurrentRoom(self.my_player)

            if direction == 'south':
                self.join_leave_message(self.my_player, 'left')
                self.my_player.current_room = self.my_dungeon.room[self.my_player.current_room].south
                self.join_leave_message(self.my_player, 'joined')
                return self.my_dungeon.DisplayCurrentRoom(self.my_player)

            if direction == 'west':
                self.join_leave_message(self.my_player, 'left')
                self.my_player.current_room = self.my_dungeon.room[self.my_player.current_room].west
                self.join_leave_message(self.my_player, 'joined')
                return self.my_dungeon.DisplayCurrentRoom(self.my_player)

            if direction == 'up':
                self.join_leave_message(self.my_player, 'left')
                self.my_player.current_room = self.my_dungeon.room[self.my_player.current_room].up
                self.join_leave_message(self.my_player, 'joined')
                return self.my_dungeon.DisplayCurrentRoom(self.my_player)

            if direction == 'down':
                self.join_leave_message(self.my_player, 'left')
                self.my_player.current_room = self.my_dungeon.room[self.my_player.current_room].down
                self.join_leave_message(self.my_player, 'joined')
                return self.my_dungeon.DisplayCurrentRoom(self.my_player)
        else:
            return self.handleBadInput()

    def start(self):
        self.change_state(In_game)
        return self.my_dungeon.DisplayCurrentRoom(self.my_player)

    def register(self):
        print("Changing the state to In_register")
        self.change_state(In_register)
        print(self.current_state)
        return " Write down your username and password to register"

    def in_register(self):
        print("Write down your username and password")

        username = self.split_input[0]
        password = self.split_input[1]

        salt = hashlib.md5()
        salt.update(bytes('salty mcsalt-salt', 'utf-8'))

        salt_value = salt.hexdigest()

        simple_hash = hashlib.md5()
        simple_hash.update(bytes(password + salt_value, 'utf-8'))

        salted_password = simple_hash.hexdigest()

        self.my_database.add_user(username, salted_password, salt_value)

        self.change_state(Idle)

        return " Successfully registered"

    def login(self):
        print("Changing the state to In_Login")
        self.change_state(In_Login)
        print(self.current_state)
        return " Write down your username and password to login"

    def in_login(self):
        print("Write down your username and password")

        username = self.split_input[0]
        password = self.split_input[1]

        if self.my_database.check_value("username", "users", "username", username, username) is True:
            salt = self.my_database.get_value("salt", "users", "username", username)

            simple_hash = hashlib.md5()
            simple_hash.update(bytes(password + salt, 'utf-8'))
            salted_password = simple_hash.hexdigest()
        else:
            salted_password = ''

        if self.my_database.check_value("username", "users", "username", username, username) is True:
            if self.my_database.check_value("password", "users", "username", username, salted_password) is True:
                # TO:DO Change the state to logged in state
                self.change_state(Logged_in)
                return " Successfully logged in. \n Type 'Start' to start the game."
            else:
                return " Password is incorrect. Try again"
        else:
            return " Username is incorrect. Try again"

    def exit(self):
        # ToDo: Implement exit here
        print("Cause errors... And Python")

    # Message to output if the player chooses unavailable direction to go
    def handleBadInput(self):
        return "Bad Input \n"
