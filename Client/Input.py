from cryptography.fernet import Fernet


class Input:
    def __init__(self, my_socket):
        self.my_socket = my_socket

    def player_input(self, new_input):
        current_input = new_input
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        cipher_text = cipher_suite.encrypt(bytes(current_input.encode('utf-8')))
        if self.my_socket is not None:
            self.my_socket.send(cipher_text, key)  # Hopefully send an encrypted message as intended ?
