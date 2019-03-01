from colorama import init
from colorama import Fore
init(autoreset=True)


class Input:
    def __init__(self):
        self.current_input: str = ''
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


    def player_input(self, current_input, client, dungeon):
        self.current_input = current_input
        self.current_client = client
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
            return Fore.BLUE + "You are not A Stranger anymore, You named yourself " + Fore.RED + split_input[1] + Fore.RESET

        else:
            # Chat messages
            message = Fore.RED + my_player.player_name + ': ' + Fore.GREEN + ' '.join(split_input)
            self_message = Fore.LIGHTBLUE_EX + 'Your words: ' + Fore.GREEN + ' '.join(split_input)
            client.send(self_message.encode())
            clients_in_room = self.check_room_for_players(my_player)
            for client in clients_in_room:
                client.send(message.encode())
            return

    # Message to output whether the player has left or joined the room
    def join_leave_message(self, player, join_or_leave):
        clients_in_the_room = self.check_room_for_players(player)
        message_output = player.player_name + " has " + join_or_leave + " the room..."
        for client in clients_in_the_room:
            client.send(message_output.encode())

    # Message to output if the player chooses unavailable direction to go
    def handleBadInput(self):
        return "Bad Input \n"