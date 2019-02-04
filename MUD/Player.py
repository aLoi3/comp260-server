class Stats:
    def __init__(self, player, strength=1, dexterity=1, vitality=1, hearing=1, observation=1):
        self.myCharacter = player
        self.str = strength
        self.dex = dexterity
        self.vit = vitality
        self.hearing = hearing
        self.observation = observation


class Attack:
    def __init__(self, attack):
        self.attack = attack


class Defence:
    def __init__(self, defence):
        self.defence = defence
