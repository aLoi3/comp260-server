from Room import Room


class Dungeon:
    def __init__(self):
        self.currentRoom = 0
        self.room = {}

    def Init(self):
        print("You've decided to go on an adventure. \n "
              "Luckily, first dungeon was nearby, which wasn't looking as dangerous as others were talking about. \n "
              "So, there you are, at the entrance to a pyramid-like dungeon! \n")

        self.room["1-entrance"] = Room("1-entrance",
                                       "There is a sign reading - DO NOT ENTER - What's your next move? \n",
                                       "1-hall", "", "", "")
        self.room["1-hall"] = Room("1-hall",
                                   "You've entered the dungeon. but suddenly, as soon as you've entered it, the doors behind you closed. \n What is you next move? \n",
                                   "1-northHallway", "", "", "")
        self.room["1-northHallway"] = Room("1-northHallway",
                                           "In front of you is a narrow corridor going only forwards \n ",
                                           "1-branching", "", "", "")
        self.room["1-branching"] = Room("1-branching",
                                        "You've encountered different ways to go. What is your next move? \n ",
                                        "1-branchingN", "1-branchingE", "1-northHallway", "1-branchingW")
        self.room["1-branchingN"] = Room("1-branchingN", "", "", "", "", "")
        self.room["1-branchingE"] = Room("1-branchingE", "", "", "", "", "")
        self.room["1-branchingW"] = Room("1-branchingW", "", "", "", "", "")

        self.currentRoom = "1-entrance"

    def DisplayCurrentRoom(self):
        print(self.room[self.currentRoom].description)

        print("Exits \n")
        exits = ["NORTH", "EAST", "SOUTH", "WEST"]
        exit = ""
        for i in exits:
            if self.room[self.currentRoom].HasExit(i.lower()):
                exit += i + " "
        print(exit)

    def isValidMove(self, direction):
        return self.room[self.currentRoom].HasExit(direction)

    def Move(self, direction):
        if self.isValidMove(direction):
            if direction == "north":
                self.currentRoom = self.room[self.currentRoom].north
                return

            if direction == "east":
                self.currentRoom = self.room[self.currentRoom].east
                return

            if direction == "south":
                self.currentRoom = self.room[self.currentRoom].south
                return

            if direction == "west":
                self.currentRoom = self.room[self.currentRoom].west
                return
