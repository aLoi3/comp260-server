class Player:

    def __init__(self, dungeon, starting_room):
        self.dungeon = dungeon
        self.current_room: str = starting_room
        self.player_id: int = 0
        self.inventory = {}
        self.equipped = {}
        self.player_name = 'aLoi3'