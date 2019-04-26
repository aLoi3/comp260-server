class Input:
    def __init__(self, my_socket):
        self.my_socket = my_socket
        self.current_input = ''

    def player_input(self, new_input):
        self.current_input = new_input
        if self.my_socket is not None:
            self.my_socket.send(self.current_input.encode())