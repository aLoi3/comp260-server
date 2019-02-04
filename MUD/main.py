from Dungeon import Dungeon
from Commands import Commands



class SUD:
    def __init__(self):
        self.myDungeon = 0
        self.commands = 0

    def Run(self):
        self.myDungeon = Dungeon()
        self.commands = Commands()
        self.myDungeon.Init()

        while True:
            self.Process()

    def Process(self):
        self.myDungeon.DisplayCurrentRoom()

        key = input("-")

        user_input = key.split(' ')

        user_input = [x for x in user_input if x != '']

        if user_input[0].lower() == 'help':
            print("HELP!!")
        elif user_input[0].lower() == 'go':
            if self.commands.isValidMove(user_input[1].lower()):
                self.commands.Move(user_input[1].lower())
            else:
                self.handleBadInput()
        else:
            self.handleBadInput()

def handleBadInput(self):
    print("\nERROR")
    print("Press any key to continue")
    input()

if __name__ == '__main__':
    sud = SUD()
    sud.Run()
