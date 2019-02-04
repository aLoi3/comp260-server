from Dungeon import Dungeon


class Commands(Dungeon):
    def __init__(self):
        Dungeon.__init__(self)

    def isValidMove(self, direction):
        return self.room[self.currentRoom].hasExit(direction)

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
