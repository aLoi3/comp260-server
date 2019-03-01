class Input:
    def __init__(self, my_socket):
        self.my_socket = my_socket

    def player_input(self, new_input):
        current_input = new_input
        if self.my_socket is not None:
            self.my_socket.send(current_input.encode())
