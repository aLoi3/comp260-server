class Room:
    # Initialise rooms
    def __init__(self, name, description, north='', east='', south='', west='', up='', down=''):
        self.name = name
        self.description = description
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.up = up
        self.down = down

    # Check if the direction player wants to go is available/has exits
    def HasExit(self, direction):
        if(direction == 'north') and (self.north != ""):
            return True

        if(direction == 'east') and (self.east != ""):
            return True

        if(direction == 'south') and (self.south != ""):
            return True

        if(direction == 'west') and (self.west != ""):
            return True

        return False
