import Input
import Window

import sys
import socket
import threading
import time
import json

from base64 import b64decode

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from PyQt5.QtWidgets import QApplication

Local_Host = False


class Client:

    def __init__(self):
        self.is_connected = False
        self.my_socket = None
        self.is_running = True
        self.app = QApplication(sys.argv)
        self.my_window = Window.Window()
        self.input_manager = ''
        self.client = ''
        self.my_connection_thread = ''
        self.my_receive_thread = ''

    def set_client(self, new_client):
        self.client = new_client
        self.my_window.set_client(self.client)

    def receive_thread(self):
        while self.is_running:
            if self.is_connected:
                try:
                    packet_id = self.my_socket.recv(10)

                    if packet_id.decode('utf-8') == 'PyramidMUD':
                        payload_size = int.from_bytes(self.my_socket.recv(2), 'little')
                        payload_data = self.my_socket.recv(payload_size)
                        data = json.loads(payload_data)
                        iv = b64decode(data['iv'])
                        cipher_text = b64decode(data['cipher_text'])

                        byte_key = self.input_manager.encryption_key.encode('utf-8')
                        byte_key = b64decode(byte_key)

                        cipher = AES.new(byte_key, AES.MODE_CBC, iv)
                        decrypted_message = unpad(cipher.decrypt(cipher_text), AES.block_size)

                        self.my_window.message_queue.put(decrypted_message.decode('utf-8'))

                    elif packet_id.decode('utf-8') == 'SettingUp!':
                        payload_size = int.from_bytes(self.my_socket.recv(2), 'little')
                        payload_data = self.my_socket.recv(payload_size)

                        key = json.loads(payload_data)
                        self.input_manager.encryption_key = key['key']
                except socket.error:
                    self.my_socket = None
                    self.is_connected = False
                    self.my_window.textEdit.append("Server Lost")
                    time.sleep(2)

    def connect_thread(self):
        while self.is_running:
            while self.is_connected is False:
                if self.my_socket is None:
                    self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                try:
                    if Local_Host:
                        self.my_socket.connect(("127.0.0.1", 8222))
                    else:
                        self.my_socket.connect(("46.101.56.200", 9284))

                    self.is_connected = True
                    self.input_manager.my_socket = self.my_socket
                    self.my_window.textEdit.append("Connected to Server \n")
                    self.my_window.textEdit.append(" Type 'Register' to create an account or "
                                                   "'Login' to login into the game. \n")
                    time.sleep(2)

                except socket.error:
                    self.is_connected = False
                    self.my_window.textEdit.append("Connection failed. Trying again")
                    time.sleep(2)

    def main(self):
        self.my_connection_thread = threading.Thread(target=self.connect_thread)
        self.my_connection_thread.start()

        self.my_receive_thread = threading.Thread(target=self.receive_thread)
        self.my_receive_thread.start()

        self.input_manager = Input.Input(self.my_socket)

        self.my_window.input_manager = self.input_manager

        self.my_window.window_draw()

        sys.exit(self.app.exec_())


if __name__ == '__main__':
    client = Client()
    client.set_client(client)
    client.main()
