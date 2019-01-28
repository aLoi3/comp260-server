action = input("What is your action? \n")

if action.lower() == "move":
    move = input("What direction?")
    if move.lower() == "right":
        print("You entered went to the right room")
    elif move.lower() == "left":
        print("There is no room on the left")
    elif move.lower() == "up":
        print("Entered a room")
    elif move.lower() == "down":
        print("Entered a room")
    else:
        print("Wrong input")
elif action.lower() == "search":
    print("Nothing has been found")
else:
    print("Wrong input")
