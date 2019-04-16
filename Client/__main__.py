import Input
import Window

import sys
import socket
import threading
import time

from PyQt5.QtWidgets import QApplication

from colorama import init
from colorama import Fore
init(autoreset=True)


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
                    self.my_window.message_queue.put(self.my_socket.recv(4096).decode("utf-8"))
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
                    self.my_socket.connect(("127.0.0.1", 8222))
                    self.is_connected = True
                    self.input_manager.my_socket = self.my_socket
                    self.my_window.textEdit.append("Connected to Server")
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
