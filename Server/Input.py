from colorama import init
from colorama import Fore
init(autoreset=True)


class Input:
    def __init__(self):
        self.current_input: str = ''
        self.all_connected_clients = ''
        self.current_client = ''

    def check_room_for_players(self, my_player):
        clients_in_room = {}
        for client in self.all_connected_clients:
            new_player = self.all_connected_clients.get(client)
            if my_player.current_room is new_player.current_room:
                if client is not self.current_client:
                    clients_in_room[client] = 0

        return clients_in_room

    def print_help(self):
        return " Possible commands: \n go <direction> \n Directions: NORTH, SOUTH, EAST, WEST \n" \
               " NOTE: If you are not using any of the commands, it will be a normal text and everyone in the room will hear it. \n" \
               " "

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

        elif command == 'go':
            if my_dungeon.room[my_player.current_room].HasExit(direction):
                if direction == 'north':
                    my_player.current_room = my_dungeon.room[my_player.current_room].north
                    return my_dungeon.DisplayCurrentRoom(my_player)

                if direction == 'east':
                    my_player.current_room = my_dungeon.room[my_player.current_room].east
                    return my_dungeon.DisplayCurrentRoom(my_player)

                if direction == 'south':
                    my_player.current_room = my_dungeon.room[my_player.current_room].south
                    return my_dungeon.DisplayCurrentRoom(my_player)

                if direction == 'west':
                    my_player.current_room = my_dungeon.room[my_player.current_room].west
                    return my_dungeon.DisplayCurrentRoom(my_player)
            else:
                return self.handleBadInput()
        else:
            # Implement chat here
            message = Fore.RED + my_player.player_name + ': ' + Fore.GREEN + ' '.join(split_input)
            self_message = Fore.LIGHTBLUE_EX + 'Your words: ' + Fore.GREEN + ' '.join(split_input)
            client.send(self_message.encode())
            clients_in_room = self.check_room_for_players(my_player)
            for client in clients_in_room:
                client.send(message.encode())
            return

    def handleBadInput(self):
        return "Bad Input \n"
