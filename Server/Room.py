class Room:
    def __init__(self, name, description, north='', east='', south='', west=''):
        self.name = name
        self.description = description
        self.north = north
        self.east = east
        self.south = south
        self.west = west

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
