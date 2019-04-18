from Room import Room


class Dungeon:
    def __init__(self):
        self.currentRoom = 0
        self.room = {}
        self.players = {}

    def Init(self):
        self.room["1-entrance"] = Room("1-entrance",
                                       " You've decided to go on an adventure. \n "
                                       " Luckily, first dungeon was nearby, which wasn't looking as dangerous as others were talking about. \n "
                                       " So, there you are, at the entrance to a pyramid-like dungeon! \n "
                                       " There is a sign reading - DO NOT ENTER - What's your next move? \n ",
                                       north="1-hall")
        self.room["1-hall"] = Room("1-hall",
                                   " You've entered the dungeon. but suddenly, as soon as you've entered it, the doors behind you closed. \n What is you next move? \n ",
                                   north="1-northHallway")
        self.room["1-northHallway"] = Room("1-northHallway",
                                           "In front of you is a narrow corridor going only forwards. \n ",
                                           north="1-branching")
        self.room["1-branching"] = Room("1-branching",
                                        " You've encountered different ways to go. Every direction leads to a deep darkness of the dungeon where dangeour await you! \n ",
                                        east="1-branchingE", south="1-northHallway", west="1-branchingW")
        self.room["1-branchingE"] = Room("1-branchingE",
                                         " Right is the right choice, huh? Well, that's your decision, after all... This dungeon is ever unpredictable, be very careful, traveller. I will support you anytime... maybe... "
                                         " Actually... Go east from here *khm* There is no trap there, definitely *giggle* \n ",
                                         north="1-branchEN", east="1-branchEE", west="1-branching")
        self.room["1-branchingW"] = Room("1-branchingW",
                                         " Good choice, my friend. Always choose left if possible! Now, what about going left again?... \n ",
                                         north="1-branchWN", east="1-branching")
        self.room["1-branchWN"] = Room("1-branchWN",
                                       " Are you stupid? I told you to go left, not right... There was no room to the left? SO WHAT? I DON'T CARE. You could've done something... "
                                       " What do you mean nothing could be done? Oh right... I forgot... Our creator is way too lazy to make stuff *deep sigh*. Why did he even create us? Can you tell? \n ",
                                       east="1-branchWNE", south="1-branchingW")
        self.room["1-branchWNE"] = Room("1-branchWNE",
                                        " Hey, don't run from my question, you little prick... Oh look, a dead-end, what a disaster, huh! \n ",
                                        up="2-start1", west="1-branchWN")
        self.room["1-branchEN"] = Room("1-branchEN",
                                       " What did I tell you? Why don't you listen to me? *cry* \n ",
                                       north="1-branchENN", south="1-branchE")
        self.room["1-branchENN"] = Room("1-branchENN",
                                        " So you refuse to listen to me? Ehh... Now you have nowhere to go, only back and listen to me crying and yelling at you once more... God... This creator of mine *sigh* \n ",
                                        south="1-branchEN")
        self.room["1-branchEE"] = Room("1-branchEE",
                                       " Hihihi, that's right. Now you will slowly die! *EVIL LAUGH* ... *caugh*. God, I'm too old for this -.- Wait, you're fine? How? Are you cheating? Please don't... \n ",
                                       north="1-branchEEN", west="1-branchingE")
        self.room["1-branchEEN"] = Room("1-branchEEN",
                                        " Don't tell me you are still alive *inside scream*. That creator... Okay, let's forget about it. It's good you're still alive, otherwise it would've been too boring. \n ",
                                        south="1-branchEE", up="2-start2")
        self.room["2-start1"] = Room("2-start1",
                                     " Wha... Oh, I see, you can climb as well, it's a pyramid after all where your goal is to get as high up as possible. Well, let's continue then, I guess. Nothing to see here. "
                                     " Wanna warn you straight away, there is nowhere to go from now on, just because creator is la... *khm* I mean has way too much work to do. \n ",
                                     down="1-branchWNE")
        self.room["2-start2"] = Room("2-start2",
                                     " Yeah.. You are still alive, what a shame. I wanted to play with some other strangers that think they can find treasures here. But oh well, shall we continue then? "
                                     " Oh right, there is no way from here. Just because creator, one word but says so much. \n",
                                     down="1-branchEEN")

        self.currentRoom = "1-entrance"

    # Displays possible exits and description of the room when player enters one
    def DisplayCurrentRoom(self, player):

        print("Exits \n")
        exits = ["NORTH", "EAST", "SOUTH", "WEST", "UP", "DOWN"]
        exit = ""
        for i in exits:
            if self.room[player.current_room].HasExit(i.lower()):
                exit += i + " "
        print(exit)

        return self.room[player.current_room].description + "\n Exits: \n " + exit + "\n"

    # Checks if the direction is valid
    def isValidMove(self, direction):
        return self.room[self.currentRoom].HasExit(direction)


    # Move to the room in player's chosen direction
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

            if direction == "up":
                self.currentRoom = self.room[self.currentRoom].up
                return

            if direction == "down":
                self.currentRoom = self.room[self.currentRoom].down
                return
