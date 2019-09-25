import hashlib
import json

from base64 import b64encode

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

Idle = 0
In_register = 1
In_Login = 2
Logged_in = 3
In_game = 4
Character_creation = 5
Character_selection = 6
Class_selection = 7

#  ToDo: Choose a class even if the character been created but the used got disconnected (DONE)
#  ToDo: Let only one user to log in into one account (DONE)
#  ToDo: Make only register unique username (WAS DONE)
#  ToDo: Other players see sentences without spaces (DONE)


class Input:
    def __init__(self):
        self.all_connected_clients = {}
        self.current_state = {}
        self.my_database = None
        self.my_player = ''
        self.split_input = ''
        self.command = ''
        self.packet_ID = 'PyramidMUD'
        self.clients_login_area = []
        self.logged_in_users = {}
        self.logged_in_players = {}
        self.setup_packet_id = 'SettingUp!'
        self.encryption_key = ''

# =================== STATE =================== #
    def change_state(self, state, client):
        message = ''

        if state == Idle:
            for client1 in list(self.logged_in_users):
                if client1 is client:
                    self.logged_in_users.pop(client)
                    self.clients_login_area.append(client)

            message = " Type 'Register' to create an account or 'Login' to login into your existing account \n" \
                      " Type 'Exit' to try to escape from this game... \n"

        elif state == Logged_in:
            for client1 in list(self.logged_in_players):
                if client1 is client:
                    username = self.my_database.get_value(
                        "owner_username",
                        "players",
                        "player_name",
                        self.logged_in_players.get(client)
                    )
                    self.logged_in_players.pop(client)
                    self.logged_in_users[client] = username

            message = " Type 'Create' to create your character or 'Play' to start a game \n" \
                      " Type 'Exit' to try to escape from this game... \n"

        self.current_state[client] = state
        return message

# =================== ENCRYPTION MESSAGE =================== #
    def add_client_to_login_area(self, client):
        self.clients_login_area.append(client)

    def clear_client_from_lists(self, client):
        if client in self.clients_login_area:
            self.clients_login_area.remove(client)
        if client in self.logged_in_users:
            del self.logged_in_users[client]
        if client in self.logged_in_players:
            del self.logged_in_players[client]

    def send_setup_info(self, key, client):
        key = b64encode(key).decode('utf-8')
        my_dict = {'key': key}
        json_packet = json.dumps(my_dict)
        header = len(json_packet).to_bytes(2, byteorder='little')

        if client is not None:
            client.send(self.setup_packet_id.encode())
            client.send(header)
            client.send(json_packet.encode())

# =================== MESSAGE =================== #
    def output_message(self, message, client):
        cipher = AES.new(self.encryption_key, AES.MODE_CBC)
        cipher_text_bytes = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
        iv = b64encode(cipher.iv).decode('utf-8')
        cipher_text = b64encode(cipher_text_bytes).decode('utf-8')
        json_message = json.dumps({'iv': iv, 'cipher_text': cipher_text})

        header = len(json_message).to_bytes(2, byteorder='little')

        if client is not None:
            client.send(self.packet_ID.encode())
            client.send(header)
            client.send(json_message.encode())

    # Function to check if there are players in the room
    def check_room_for_players(self, client):
        clients_in_room = {}
        for other_client in self.all_connected_clients:
            other_player = self.logged_in_players.get(other_client)
            if self.my_database.get_current_room(self.logged_in_players[client]) == \
                    self.my_database.get_current_room(other_player):
                if other_client is not client:
                    clients_in_room[other_client] = 0

        return clients_in_room

    def chat_message(self, client):
        # Chat messages
        message = self.logged_in_players.get(client) + ': '
        message += ' '.join(self.split_input)
        self_message = 'Your words: ' + ' '.join(self.split_input)
        self.output_message(self_message, client)
        clients_in_room = self.check_room_for_players(client)
        for client1 in clients_in_room:
            self.output_message(message, client1)
        return

    # Message to output whether the player has left or joined the room
    def join_leave_message(self, player, join_or_leave, client):
        clients_in_the_room = self.check_room_for_players(client)
        message_output = player + " has " + join_or_leave + " the room... \n"
        for client in clients_in_the_room:
            self.output_message(message_output, client)

# =================== HELP =================== #
    def SEND_HELP(self):
        return " I will be your guide through this worst-ever-made dungeon..." \
               " That's what I think, at least. And please, read me as if it was a spooky ghost, deal? BOOooOOoo \n" \
               " Nevertheless, these are your possible commands: \n" \
               " go <direction> \n Directions: NORTH, SOUTH, EAST, WEST, UP, DOWN \n" \
               " exit - to exit the game \n" \
               " NOTE: If you are not using any of the commands, it will be a normal text and" \
               " everyone in the room will hear it. \n"

# =================== MAIN - PLAYER INPUT =================== #
    def player_input(self, current_input, client, database):
        self.my_database = database
        self.split_input = current_input.split()
        self.command = self.split_input[0].lower()
        if self.current_state.get(client) is None:
            self.change_state(Idle, client)
        message = ''

        for client1 in list(self.logged_in_players):
            if client1 is client:
                if self.current_state.get(client) == In_game:
                    if self.command == "go":
                        message = self.move(client)
                    elif self.command == "help":
                        message = self.SEND_HELP()
                    elif self.command == "exit":
                        message = self.change_state(Logged_in, client)
                    else:
                        self.chat_message(client)

                if message is not None:
                    self.output_message(message, client)
                    return

        for client1 in list(self.logged_in_users):
            if client1 is client:
                if self.current_state.get(client) == Logged_in:
                    if self.command == "create":
                        message = self.create_character(client)
                    elif self.command == "play":
                        message = self.display_characters(client)
                    elif self.command == "exit":
                        message = self.change_state(Idle, client)
                    else:
                        message = "Incorrect Input \n"

                elif self.current_state.get(client) == Character_selection:
                    message = self.choose_character(client)

                elif self.current_state.get(client) == Class_selection:
                    message = self.class_selection(client)

                elif self.current_state.get(client) == Character_creation:
                    message = self.character_creation(client)

                if message is not None:
                    self.output_message(message, client)
                    return

        for client1 in list(self.clients_login_area):
            if client1 is client:
                if self.current_state.get(client) == Idle:
                    if self.command == "register":
                        message = self.register(client)
                    elif self.command == "login":
                        message = self.login(client)
                    elif self.command == "exit":
                        message = "You cannot escape this! MUAHAHAHAHA"
                    else:
                        message = "Incorrect Input \n"

                elif self.current_state.get(client) == In_register:
                    message = self.in_register(client)

                elif self.current_state.get(client) == In_Login:
                    message = self.in_login(client)

                if message is not None:
                    self.output_message(message, client)
                    return
        #return

# =================== EXIT DISPLAY =================== #
    def display_exits(self, room):
        exits = ["NORTH", "EAST", "SOUTH", "WEST", "UP", "DOWN"]
        exit = "\nYou see exits in these directions - \n"

        all_connections = self.my_database.get_all_values("*", "dungeon", "name", room)

        for index, value in enumerate(exits):
            if all_connections[0][index + 2] is not None:
                exit += value + " "
        exit += "\n"

        return exit

# =================== MOVEMENT =================== #
    def valid_move(self, direction, client):
        current_room = self.my_database.get_current_room(self.logged_in_players.get(client))
        connection = self.my_database.get_connection(direction, current_room)

        if connection is not None:
            self.join_leave_message(self.logged_in_players.get(client), 'left', client)
            self.my_database.set_current_room(self.logged_in_players.get(client), connection)
            self.join_leave_message(self.logged_in_players.get(client), 'joined', client)
            clients_in_room = self.check_room_for_players(client)
            reply_to_player = self.my_database.get_value('description', 'dungeon', 'name', connection)
            reply_to_player += self.display_exits(connection)
            if clients_in_room:
                reply_to_player += "\n You see "
                for client1 in clients_in_room:
                    reply_to_player += self.logged_in_players.get(client1)
                reply_to_player += " in the room. \n"

            return reply_to_player
        else:
            return " There is no path this way! \n"

    def move(self, client):
        if len(self.split_input) >= 2:
            direction = self.split_input[1].lower()
        else:
            direction = ''

        if direction == 'north':
            return self.valid_move(direction, client)
        elif direction == 'east':
            return self.valid_move(direction, client)
        elif direction == 'south':
            return self.valid_move(direction, client)
        elif direction == 'west':
            return self.valid_move(direction, client)
        elif direction == 'up':
            return self.valid_move(direction, client)
        elif direction == 'down':
            return self.valid_move(direction, client)
        else:
            self.output_message(self.handleBadInput(), client)

# =================== START =================== #
    def start(self, client):
        current_room = self.my_database.get_current_room(self.logged_in_players.get(client))
        message = self.my_database.get_value('description', 'dungeon', 'name', current_room)
        message += self.display_exits(current_room)
        self.change_state(In_game, client)
        return message + "\n"

# =================== CHARACTER CREATION =================== #
    def create_character(self, client):
        self.change_state(Character_creation, client)
        return " What is your character's name going to be? \n" \
               " Note: if you want to get back to previous state, type 'Back' \n"

    def character_creation(self, client):
        if self.command == "back":
            message = self.change_state(Logged_in, client)
            return message

        nickname = self.split_input[0]
        is_name_taken = self.my_database.check_value(
            'player_name',
            'players',
            'player_name',
            nickname,
            nickname
        )
        if is_name_taken is True:
            message = " Player name is already taken \n"
            self.output_message(message, client)
        else:
            #  Add player to the database
            self.my_database.add_player(self.logged_in_users[client], "1-entrance", nickname)
            message = " " + nickname + " has been successfully created! \n"
            message += self.change_state(Logged_in, client)

        return message

    def class_selection(self, client):
        if self.command == "back":
            message = self.change_state(Logged_in, client)
            return message

        if self.command == "warrior":
            self.my_database.set_stat_value("strength", self.my_player, 3)
            self.my_database.set_stat_value("agility", self.my_player, 2)
            self.my_database.set_stat_value("player_class", self.my_player, "warrior")

            message = " You've chosen to be a warrior! \n"
        elif self.command == "rogue":
            self.my_database.set_stat_value("strength", self.my_player, 1)
            self.my_database.set_stat_value("agility", self.my_player, 3)
            self.my_database.set_stat_value("intelligence", self.my_player, 1)
            self.my_database.set_stat_value("player_class", self.my_player, "rogue")

            message = " You've chosen to be a rogue! \n"
        elif self.command == "wizard":
            self.my_database.set_stat_value("intelligence", self.my_player, 3)
            self.my_database.set_stat_value("hearing", self.my_player, 1)
            self.my_database.set_stat_value("observation", self.my_player, 1)
            self.my_database.set_stat_value("player_class", self.my_player, "wizard")

            message = " You've chosen to be a wizard! \n"
        elif self.command == "scout":
            self.my_database.set_stat_value("hearing", self.my_player, 2)
            self.my_database.set_stat_value("observation", self.my_player, 2)
            self.my_database.set_stat_value("agility", self.my_player, 1)
            self.my_database.set_stat_value("player_class", self.my_player, "scout")

            message = " You've chosen to be a scout! \n"
        elif self.command == "deprived":
            self.my_database.set_stat_value("player_class", self.my_player, "deprived")

            message = " So you like hardcore, I see... \n"
        else:
            message = " You have chosen an unexisting class. Please try again \n"

        self.logged_in_players[client] = self.my_player
        self.logged_in_users.pop(client)
        message += " Logged in as " + self.my_player + "\n"
        message += self.start(client)

        return message

# =================== CHARACTER SELECTION =================== #
    def display_characters(self, client):

        owned_player = self.my_database.get_all_values(
            'player_name',
            'players',
            'owner_username',
            self.logged_in_users.get(client)
        )

        if len(owned_player) is not 0:
            message = " Your current character(s) that you can play as are - "
            for index, val in enumerate(owned_player):
                message += owned_player[index][0]
                if not index+1 == len(owned_player):
                    message += ", "
            message += ". \n Type your character's name to start playing him. \n" \
                       " Note: if you want to get back to previous state, type 'Back' \n"
            self.change_state(Character_selection, client)
        else:
            message = " You cannot play a game without having a character, silly. Create a character first! \n"
            message += self.change_state(Logged_in, client)

        return message

    def choose_character(self, client):
        if self.command == "back":
            message = self.change_state(Logged_in, client)
            return message

        message = ''

        owned_player = self.my_database.get_all_values(
            'player_name',
            'players',
            'owner_username',
            self.logged_in_users.get(client)
        )

        if len(owned_player) is not 0:
            for index, val in enumerate(owned_player):
                if owned_player[index][0] == self.split_input[0]:

                    self.my_player = self.split_input[0]
                    user_class = self.my_database.get_value("player_class", "players", "player_name", self.my_player)

                    if user_class is None:
                        message = " You don't have a class. Choose from the following - WARRIOR, ROGUE, WIZARD, SCOUT, DEPRIVED \n"
                        self.change_state(Class_selection, client)
                    else:
                        self.logged_in_players[client] = owned_player[index][0]
                        self.logged_in_users.pop(client)
                        message = " Logged in as " + self.split_input[0] + " \n"
                        message += self.start(client)
        else:
            message = " You cannot play a game without having a character, silly \n"

        return message

# =================== REGISTRATION =================== #
    def register(self, client):
        self.change_state(In_register, client)

        return " Type your username and password to register \n" \
               " Note: if you want to get back to previous state, type 'Back' \n"

    def in_register(self, client):
        if self.command == "back":
            message = self.change_state(Idle, client)
            return message

        if len(self.split_input) >= 2:
            username = self.split_input[0].upper()
            password = self.split_input[1]
        else:
            return "Please provide username and password separated with space \n"

        if self.my_database.check_value("username", "users", "username", username, username) is True:
            return " This username has already been taken. Use another one. \n"

        salt = hashlib.md5()
        salt.update(bytes('salty mcsalt-salt', 'utf-8'))

        salt_value = salt.hexdigest()

        simple_hash = hashlib.md5()
        simple_hash.update(bytes(password + salt_value, 'utf-8'))

        salted_password = simple_hash.hexdigest()

        self.my_database.add_user(username, salted_password, salt_value)

        message = self.change_state(Idle, client)

        return " Successfully registered \n" + message

# =================== LOGIN =================== #
    def login(self, client):
        self.change_state(In_Login, client)
        return " Type your username and password to login \n" \
               " Note: if you want to get back to previous state, type 'Back' \n"

    def in_login(self, client):
        if self.command == "back":
            message = self.change_state(Idle, client)
            return message

        if len(self.split_input) >= 2:
            username = self.split_input[0].upper()
            password = self.split_input[1]
        else:
            return "Please provide username and password separated with space \n"

        if self.my_database.check_value("username", "users", "username", username, username) is True:
            salt = self.my_database.get_value("salt", "users", "username", username)

            simple_hash = hashlib.md5()
            simple_hash.update(bytes(password + salt, 'utf-8'))
            salted_password = simple_hash.hexdigest()
        else:
            salted_password = ''

        if self.my_database.check_value("username", "users", "username", username, username) is True:
            if self.my_database.check_value("password", "users", "username", username, salted_password) is True:
                if len(self.logged_in_users) is not 0:
                    for user in list(self.logged_in_users):
                        un = self.logged_in_users.get(user)
                        if username != un:
                            self.logged_in_users[client] = username
                            self.clients_login_area.remove(client)
                            message = self.change_state(Logged_in, client)
                            return " Successfully logged in. \n" + message
                        else:
                            return " This account is already in use. Try again later. \n"
                else:
                    self.logged_in_users[client] = username
                    self.clients_login_area.remove(client)
                    message = self.change_state(Logged_in, client)
                    return " Successfully logged in. \n" + message
        else:
            return " Username is incorrect. Try again \n"

# =================== RUN AWAY =================== #
    def exit(self):
        # ToDo: Implement exit here
        return "You cannot escape it now... HAHAHAHA \n"

# =================== FOR NO REASON =================== #
    # Message to output if the player chooses unavailable direction to go
    def handleBadInput(self):
        return "Bad Input \n"
