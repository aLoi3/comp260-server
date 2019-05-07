import hashlib
import json

from base64 import b64encode

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


# ToDo: Implement a back function; (DONE)
# ToDo: Display exits; (DONE)
# ToDo: Exit the game;
# ToDo: Display messages in correct order; (DONE)
# ToDo: Change the way I set the current player (In register and character selection) (DONE)
# ToDo: Support multiple clients - There's only one client that can play the game  - It IS supporting, but needs fixing
# ToDo: Fix chat system (DONE)
# ToDo: Crashes when not providing a password for register (DONE)
# ToDo: Data Encryption (DONE)

Idle = 0
In_register = 1
In_Login = 2
Logged_in = 3
In_game = 4
Character_creation = 5
Character_selection = 6


class Input:
    def __init__(self):
        self.all_connected_clients = {}
        self.current_client = ''
        self.current_state = Idle
        self.my_database = None
        self.my_dungeon = None
        self.my_player = None
        self.split_input = ''
        self.command = ''
        self.connected_username = ''
        self.connected_player = ''
        self.packet_ID = 'PyramidMUD'
        self.clients_login_area = []
        self.clients_play_area = []
        self.logged_in_users = {}
        self.setup_packet_id = 'SettingUp!'
        self.encryption_key = ''

# =================== STATE =================== #
    def change_state(self, state):
        message = ''

        if state == Idle:
            message = " Type 'Register' to create an account or 'Login' to login into your existing account \n" \
                      " Type 'Exit' to try to escape from this game... \n"
        elif state == Logged_in:
            message = " Type 'Create' to create your character or 'Play' to start a game \n" \
                      " Type 'Exit' to try to escape from this game... \n"

        self.current_state = state
        return message

# =================== ENCRYPTION MESSAGE =================== #
    def add_client_to_login_area(self, client):
        self.clients_login_area.append(client)

    def clear_client_from_lists(self, client):
        if client in self.clients_login_area:
            self.clients_login_area.remove(client)
        if client in self.clients_play_area:
            self.clients_play_area.remove(client)
        if client in self.logged_in_users:
            del self.logged_in_users[client]

    def send_setup_info(self, key, client):
        key = b64encode(key).decode('utf-8')
        my_dict = {'key': key}
        json_packet = json.dumps(my_dict)
        header = len(json_packet).to_bytes(2, byteorder='little')

        if self.current_client is not None:
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
    def check_room_for_players(self):
        clients_in_room = {}
        for other_client in self.all_connected_clients:
            other_player = self.all_connected_clients.get(other_client)
            if self.my_database.get_current_room(self.my_player) == \
                    self.my_database.get_current_room(other_player):
                if other_client is not self.current_client:
                    clients_in_room[other_client] = 0

        return clients_in_room

    def chat_message(self):
        # Chat messages
        message = self.my_player + ': '
        message += ''.join(self.split_input)
        self_message = 'Your words: ' + ' '.join(self.split_input)
        self.output_message(self_message, self.current_client)
        clients_in_room = self.check_room_for_players()
        for client in clients_in_room:
            self.output_message(message, client)
        return

    # Message to output whether the player has left or joined the room
    def join_leave_message(self, player, join_or_leave):
        clients_in_the_room = self.check_room_for_players()
        message_output = player + " has " + join_or_leave + " the room..."
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
               " everyone in the room will hear it. \n" \


# =================== MAIN - PLAYER INPUT =================== #
    def player_input(self, current_input, client, dungeon, database):
        self.current_client = client
        self.my_database = database
        self.my_dungeon = dungeon
        # self.all_connected_clients[client] = client
        self.my_player = self.all_connected_clients.get(client)

        self.split_input = current_input.split()
        self.command = self.split_input[0].lower()
        message = ''

        if self.current_state == Idle:
            for client in self.all_connected_clients:
                if client is not current_input:
                    self.all_connected_clients[client] = client

            if self.command == "register":
                message = self.register()
            elif self.command == "login":
                message = self.login()
            elif self.command == "exit":
                message = "You cannot escape this! MUAHAHAHAHA"
            else:
                message = "Incorrect Input"

        elif self.current_state == In_register:
            message = self.in_register()

        elif self.current_state == In_Login:
            message = self.in_login()

        elif self.current_state == Logged_in:
            if self.command == "create":
                message = self.create_character()
            elif self.command == "play":
                message = self.display_characters()
            elif self.command == "exit":
                message = self.change_state(Idle)
            else:
                message = "Incorrect Input"

        elif self.current_state == Character_selection:
            message = self.choose_character()

        elif self.current_state == In_game:
            if self.command == "go":
                message = self.move()
            elif self.command == "help":
                message = self.SEND_HELP()
            elif self.command == "exit":
                message = self.change_state(Logged_in)
            else:
                self.chat_message()

        elif self.current_state == Character_creation:
            message = self.character_creation()

        if self.command == "exit":
            self.exit()

        self.output_message(message, self.current_client)

# =================== LOST IN ACTION =================== #
    def change_name(self):
        self.my_player.player_name = self.split_input[1]
        return "You are no more a stranger, You named yourself " + self.split_input[1]

# =================== EXIT DISPLAY =================== #
    def display_exits(self, room):
        exits = ["NORTH", "EAST", "SOUTH", "WEST", "UP", "DOWN"]
        exit = "\nYou see exits in these directions - \n"

        all_connections = self.my_database.get_all_values("*", "dungeon", "name", room)

        for index, value in enumerate(exits):
            if all_connections[0][index + 2] is not None:
                exit += value + " "

        return exit

# =================== MOVEMENT =================== #
    def valid_move(self, direction):
        current_room = self.my_database.get_current_room(self.my_player)
        connection = self.my_database.get_connection(direction, current_room)

        if connection is not None:
            self.join_leave_message(self.my_player, 'left')
            self.my_database.set_current_room(self.my_player, connection)
            self.join_leave_message(self.my_player, 'joined')
            clients_in_room = self.check_room_for_players()
            reply_to_player = self.my_database.get_value('description', 'dungeon', 'name', connection)
            reply_to_player += self.display_exits(connection)
            if clients_in_room:
                reply_to_player += "You see "
                for client in clients_in_room:
                    reply_to_player += self.all_connected_clients.get(client)
                reply_to_player += " in the room. \n"

            return reply_to_player
        else:
            return " There is no path this way! \n"

    def move(self):
        if len(self.split_input) >= 2:
            direction = self.split_input[1].lower()
        else:
            direction = ''

        if direction == 'north':
            return self.valid_move(direction)
        elif direction == 'east':
            return self.valid_move(direction)
        elif direction == 'south':
            return self.valid_move(direction)
        elif direction == 'west':
            return self.valid_move(direction)
        elif direction == 'up':
            return self.valid_move(direction)
        elif direction == 'down':
            return self.valid_move(direction)
        else:
            self.output_message(self.handleBadInput(), self.current_client)

# =================== START =================== #
    def start(self):
        current_room = self.my_database.get_current_room(self.my_player)
        message = self.my_database.get_value('description', 'dungeon', 'name', current_room)
        message += self.display_exits(current_room)
        self.change_state(In_game)
        return message + "\n"

# =================== CHARACTER CREATION =================== #
    def create_character(self):
        self.change_state(Character_creation)
        return " What is your character's name going to be? \n" \
               " Note: if you want to get back to previous state, type 'Back' \n"

    def character_creation(self):
        if self.command == "back":
            message = self.change_state(Logged_in)
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
        else:
            self.my_database.add_player(self.my_player, "1-entrance", nickname)
            message = " " + nickname + " has been successfully created! \n"
            message += self.change_state(Logged_in)

        return message

# =================== CHARACTER SELECTION =================== #
    def display_characters(self):
        owned_player = self.my_database.get_all_values(
            'player_name',
            'players',
            'owner_username',
            self.my_player
        )

        if len(owned_player) is not 0:
            message = " Your current character(s) that you can play as are - "
            for index, val in enumerate(owned_player):
                message += owned_player[index][0]
                if not index+1 == len(owned_player):
                    message += ", "
            message += ". \n Type your character's name to start playing him. \n" \
                       " Note: if you want to get back to previous state, type 'Back' \n"
            self.change_state(Character_selection)
        else:
            message = " You cannot play a game without having a character, silly. Create a character first! \n"
            message += self.change_state(Logged_in)

        return message

    def choose_character(self):
        if self.command == "back":
            message = self.change_state(Logged_in)
            return message

        message = ''
        player_is_owned = False

        owned_player = self.my_database.get_all_values(
            'player_name',
            'players',
            'owner_username',
            self.my_player  # connected_username
        )

        if len(owned_player) is not 0:
            for index, val in enumerate(owned_player):
                if owned_player[index][0] == self.split_input[0]:
                    player_is_owned = True
                    # self.my_player = owned_player[index][0]
                    # message = self.start()
        else:
            message = " You cannot play a game without having a character, silly \n"

        if player_is_owned:
            for client in self.all_connected_clients:
                self.all_connected_clients[client] = self.split_input[0]
                self.my_player = self.split_input[0]
                self.clients_play_area.append(self.current_client)
                self.clients_login_area.remove(self.current_client)

            message = ' Logged in as ' + self.split_input[0] + ' \n'
            message += self.start()
        else:
            message = ' You cannot play a character you do not own \n'

        return message

# =================== REGISTRATION =================== #
    def register(self):
        self.change_state(In_register)
        return " Type your username and password to register \n" \
               " Note: if you want to get back to previous state, type 'Back' \n"

    def in_register(self):
        if self.command == "back":
            message = self.change_state(Idle)
            return message

        if len(self.split_input) >= 2:
            username = self.split_input[0].upper()
            password = self.split_input[1]
        else:
            return "Please provide username and password separated with space \n"

        salt = hashlib.md5()
        salt.update(bytes('salty mcsalt-salt', 'utf-8'))

        salt_value = salt.hexdigest()

        simple_hash = hashlib.md5()
        simple_hash.update(bytes(password + salt_value, 'utf-8'))

        salted_password = simple_hash.hexdigest()

        self.my_database.add_user(username, salted_password, salt_value)

        message = self.change_state(Idle)

        return " Successfully registered \n" + message

# =================== LOGIN =================== #
    def login(self):
        self.change_state(In_Login)
        return " Type your username and password to login \n" \
               " Note: if you want to get back to previous state, type 'Back' \n"

    def in_login(self):
        for client in self.all_connected_clients:
            if client in self.clients_login_area:
                if self.command == "back":
                    message = self.change_state(Idle)
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
                        # self.connected_username = username
                        self.all_connected_clients[client] = username
                        self.logged_in_users[client] = self.my_player
                        message = self.change_state(Logged_in)
                        return " Successfully logged in. \n" + message
                    else:
                        return " Password is incorrect. Try again \n"
                else:
                    return " Username is incorrect. Try again \n"

# =================== RUN AWAY =================== #
    def exit(self):
        # ToDo: Implement exit here
        return
        #sys.exit(0)

# =================== FOR NO REASON =================== #
    # Message to output if the player chooses unavailable direction to go
    def handleBadInput(self):
        return "Bad Input \n"
