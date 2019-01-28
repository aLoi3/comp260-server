actions = ["move", "go", "search", "look"]
directions = ["up", "down", "right", "left"]

action = input("What is your action? \n")

if action.lower() == actions[0] or action.lower() == actions[1]:
    move = input("What direction? \n")
    if move.lower() == directions[0]:
        print("You entered went to the right room")
    elif move.lower() == directions[1]:
        print("There is no room on the left")
    elif move.lower() == directions[2]:
        print("Entered a room")
    elif move.lower() == directions[3]:
        print("Entered a room")
    else:
        print("Wrong input")
elif action.lower() == actions[2] or action.lower() == actions[3]:
    print("Nothing has been found")
else:
    print("Wrong input")
