class Room:
    def __init__(self, name, description, north, east, south, west):
        self.name = name
        self.description = description
        self.north = north
        self.east = east
        self.south = south
        self.west = west

    def HasExit(self, direction):
        if(direction.lower() == 'north') and (self.north != ""):
            return True

        if(direction.lower() == 'east') and (self.east != ""):
            return True

        if(direction.lower() == 'south') and (self.south != ""):
            return True

        if(direction.lower() == 'west') and (self.west != ""):
            return True

        return False
