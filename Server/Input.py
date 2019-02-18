from Dungeon import Dungeon


class Input:
    def __init__(self):
        self.current_input: str = ''
        self.all_connected_client = ''

    def print_help(self):
        print("Possible commands: \n"
              "go <direction> \n"
              "Directions: NORTH, SOUTH, EAST, WEST \n")

    def player_input(self, current_input, player, dungeon):
        self.current_input = current_input
        my_dungeon = dungeon
        my_player = player
        #self.my_dungeon.DisplayCurrentRoom()

        split_input = current_input.split(' ', 1).lower()
        command = split_input[0].lower()
        direction = split_input[1].lower()

        if command == 'help':
            self.print_help()

        elif command == 'go':
            if self.my_dungeon.isValidMove(direction):
                self.my_dungeon.Move(direction)
            else:
                self.handleBadInput()
        else:
            # Implement chat here
            message = my_player.player_name + ': '
            message += ''.join(split_input)
            for client in self.all_connected_client:
                client.send(message.encode())
            #return


    def handleBadInput(self):
        print("Bad Input \n")
        print("Press any key to continue \n")
        input()
