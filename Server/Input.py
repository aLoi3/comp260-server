class Input:
    def __init__(self):
        self.current_input: str = ''
        self.all_connected_client = ''

    def print_help(self):
        return " Possible commands: \n go <direction> \n Directions: NORTH, SOUTH, EAST, WEST \n"

    def player_input(self, current_input, player, dungeon):
        self.current_input = current_input
        my_dungeon = dungeon
        my_player = player
        #my_dungeon.DisplayCurrentRoom()

        split_input = current_input.split(' ', 1)
        command = split_input[0].lower()
        if len(split_input) >= 2:
            direction = split_input[1].lower()
        else:
            direction = ''

        if command == 'p':
            return my_dungeon.DisplayCurrentRoom()

        elif command == 'help':
            return self.print_help()

        elif command == 'go':
            if my_dungeon.room[my_dungeon.currentRoom].HasExit(direction):
                if direction == 'north':
                    my_dungeon.currentRoom = my_dungeon.room[my_dungeon.currentRoom].north
                    return my_dungeon.room[my_dungeon.currentRoom].description

                if direction == 'east':
                    my_dungeon.currentRoom = my_dungeon.room[my_dungeon.currentRoom].east
                    return my_dungeon.room[my_dungeon.currentRoom].description

                if direction == 'south':
                    my_dungeon.currentRoom = my_dungeon.room[my_dungeon.currentRoom].south
                    return my_dungeon.room[my_dungeon.currentRoom].description

                if direction == 'west':
                    my_dungeon.currentRoom = my_dungeon.room[my_dungeon.currentRoom].west
                    return my_dungeon.room[my_dungeon.currentRoom].description
            else:
                return self.handleBadInput()
        else:
            # Implement chat here
            message = my_player.player_name + ': '
            message += ''.join(split_input)
            for client in self.all_connected_client:
                client.send(message.encode())
            return

    def handleBadInput(self):
        return "Bad Input \n"
