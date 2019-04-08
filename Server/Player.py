class Player:

    def __init__(self, dungeon, starting_room):
        self.dungeon = dungeon
        self.current_room = starting_room
        self.player_id = 0
        self.inventory = {}
        self.equipped = {}
        self.player_name = 'A Stranger'
