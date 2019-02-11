from Dungeon import Dungeon


class Command():
    def __init__(self):
        self.myDungeon = Dungeon()

    def isValidMove(self, direction):
        return self.myDungeon.room[self.myDungeon.currentRoom].HasExit(direction)

    def Move(self, direction):
        if self.isValidMove(direction):
            if direction == "north":
                self.myDungeon.currentRoom = self.myDungeon.room[self.myDungeon.currentRoom].north
                return

            if direction == "east":
                self.myDungeon.currentRoom = self.myDungeon.room[self.myDungeon.currentRoom].east
                return

            if direction == "south":
                self.myDungeon.currentRoom = self.myDungeon.room[self.myDungeon.currentRoom].south
                return

            if direction == "west":
                self.myDungeon.currentRoom = self.myDungeon.room[self.myDungeon.currentRoom].west
                return
