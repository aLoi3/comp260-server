class Input:
    def __init__(self, my_socket):
        self.lowered_input = ''
        self.my_socket = my_socket

    def player_input(self, my_socket):
        current_input = input('> ')
        self.lowered_input = current_input
        my_socket.send(self.lowered_input.encode())
