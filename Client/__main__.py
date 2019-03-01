from queue import *
import socket
import sys
import threading
import time
import Input

from colorama import init
from colorama import Fore
init(autoreset=True)

message_queue = Queue()
is_connected = False
my_socket = None
is_running = True


def receive_thread(server_socket):
    global is_connected
    global is_running
    global my_socket

    while is_running:
        if is_connected:
            try:
                message_queue.put(server_socket.recv(4096).decode("utf-8"))
                # print("Adding to queue")
            except socket.error:
                my_socket = None
                is_connected = False
                print("Server lost")


def main():
    global is_connected
    global my_socket
    global is_running

    input_manager = Input.Input(my_socket)

    while is_running:
        while not is_connected:

            if my_socket is None:
                my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                my_receive_thread = threading.Thread(target=receive_thread, args=(my_socket,))
                my_receive_thread.start()

            try:
                my_socket.connect(("127.0.0.1", 8222))
                is_connected = True
                print("Connected to Server")
                print(Fore.BLUE + "Type 'Start' to Begin Your Journey!" + Fore.RESET)
            except socket.error:
                is_connected = False
                print("Couldn't connect to Server, trying again in 2 seconds")
                time.sleep(2)

        while is_connected:
            try:
                input_manager.player_input(my_socket)
                time.sleep(0.5)
            except socket.error:
                print("Server lost. Trying to reconnect")
                is_connected = False
                my_socket = None

            while message_queue.qsize() > 0:
                print(message_queue.get())

    print("Exiting")
    my_socket.close()


if __name__ == '__main__':
    main()
