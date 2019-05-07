import bcrypt
import json

from base64 import b64encode
from base64 import b64decode

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


class Input:
    def __init__(self, my_socket):
        self.my_socket = my_socket
        self.current_input = ''
        self.password = ''
        self.username = ''
        self.salt = ''
        self.packed_ID = 'PyramidMUD'
        self.encryption_key = ''

    def set_salt(self, salt):
        self.salt = salt

    def set_username_password(self, username, password):
        self.username = username
        self.password = password

    def send_username(self):
        message = '#username ' + self.username
        self.player_input(message)

    def send_password(self):
        self.password = self.password.encode('utf-8')
        self.salt = self.salt.encode('utf-8')
        self.password = bcrypt.hashpw(self.password, self.salt)
        self.password = self.password.decode()
        message = '#username_salt ' + self.password
        self.player_input(message)

    def player_input(self, new_input):
        byte_key = self.encryption_key.encode('utf-8')
        byte_key = b64encode(byte_key)

        cipher = AES.new(byte_key, AES.MODE_CBC)
        cipher_text_bytes = cipher.encrypt(pad(new_input.encode('utf-8'), AES.block_size))

        iv = b64encode(cipher_text_bytes).decode('utf-8')
        cipher_text = b64encode(cipher_text_bytes).decode('utf-8')
        json_message = json.dumps({'iv': iv, 'cipher_text': cipher_text})

        header = len(json_message).to_bytes(2, byteorder='little')

        if self.my_socket is not None:
            self.my_socket.send(self.packed_ID.encode())
            self.my_socket.send(header)
            self.my_socket.send(json_message.encode())
