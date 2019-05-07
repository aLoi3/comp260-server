import socket
import threading
import time
import json

from base64 import b64decode
from queue import *

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes

import Input
import Dungeon
import Player
import Database

encryption_key = get_random_bytes(16)
clients = {}
clients_lock = threading.Lock()
lost_clients = []
message_queue = Queue()


def receive_thread(client_socket):
    receive_is_running = True
    while receive_is_running:
        try:
            packet_id = client_socket.recv(10)
            if packet_id.decode('utf-8') == "PyramidMUD":
                payload_size = int.from_bytes(client_socket.recv(2), 'little')
                payload_data = client_socket.recv(payload_size)
                payload_data = payload_data.decode('utf-8')

                data = json.loads(payload_data)

                iv = b64decode(data['iv'])
                cipher_text = b64decode(data['cipher_text'])
                cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
                decrypted_message = unpad(cipher.decrypt(cipher_text), AES.block_size)

                message_queue.put((client_socket, decrypted_message.decode('utf-8')))

        except socket.error:
            print("Client lost")
            lost_clients.append(client_socket)
            receive_is_running = False


def accept_clients(server_socket):
    while is_running:
        print("Looking for new clients")
        new_client = server_socket.accept()
        print("Added client. Socket info: " + str(new_client[0]))
        clients_lock.acquire()
        clients[new_client[0]] = 0  # Player.Player(my_dungeon, '1-entrance')
        my_receive_thread = threading.Thread(target=receive_thread, args=(new_client[0], ))
        my_receive_thread.start()

        input_manager.send_setup_info(encryption_key, new_client[0])
        input_manager.all_connected_clients[new_client[0]] = 0
        input_manager.add_client_to_login_area(new_client[0])
        clients_lock.release()


if __name__ == '__main__':

    is_running = True
    is_connected = False

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind(("127.0.0.1", 8222))
    #  my_socket.bind(("46.101.56.200", 9284))
    my_socket.listen(5)

    my_dungeon = Dungeon.Dungeon()
    # my_dungeon.Init()
    # my_player = Player.Player(my_dungeon, '1-entrance')
    input_manager = Input.Input()
    input_manager.encryption_key = encryption_key

    my_database = Database.Database()

    my_accept_thread = threading.Thread(target=accept_clients, args=(my_socket, ))
    my_accept_thread.start()

    while is_running is True:
        client_and_message = ''

        clients_lock.acquire()

        while message_queue.qsize() > 0:
            try:
                client_and_message = message_queue.get()
                client_reply = input_manager.player_input(
                    client_and_message[1],
                    client_and_message[0],
                    my_dungeon,
                    my_database
                )
                if client_reply is not None:
                    input_manager.output_message(client_reply, client_and_message[0])
                    # client_and_message[0].send(client_reply.encode())

            except socket.error:
                lost_clients.append(client_and_message[0])
                print("Client lost")

        for client in lost_clients:
            clients.pop(client)
            input_manager.clear_client_from_lists(client)
            input_manager.all_connected_clients = clients

        lost_clients = []

        clients_lock.release()

        time.sleep(0.5)
