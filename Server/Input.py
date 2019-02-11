from Dungeon import Dungeon


class Input:
    def __init__(self):
        self.my_dungeon = 0

    def print_help(self):
        print("Possible commands: \n"
              "go <direction> \n"
              "Directions: NORTH, SOUTH, EAST, WEST \n")

    def player_input(self):
        self.my_dungeon = Dungeon()
        self.my_dungeon.DisplayCurrentRoom()

        key = input("-")

        user_input = key.split(' ')

        user_input = [x for x in user_input if x != '']

        if user_input[0].lower() == 'help':
            self.print_help()
        elif user_input[0].lower() == 'go':
            if self.my_dungeon.isValidMove(user_input[1].lower()):
                self.my_dungeon.Move(user_input[1].lower())
            else:
                self.handleBadInput()
        else:
            self.handleBadInput()

    def handleBadInput(self):
        print("\nBad Input")
        print("Press any key to continue")
        input()
