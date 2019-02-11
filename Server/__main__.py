import socket
import threading
import time

import Input
import Dungeon
import Player

clients = {}
clients_lock = threading.Lock()


def accept_clients(server_socket):
    while isRunning:
        print("Looking for new clients")
        new_client = server_socket.accept()
        print("Added client. Socket info: " + str(new_client[0]))
        clients_lock.acquire()
        clients[new_client[0]] = 0
        clients_lock.release()


if __name__ == '__main__':

    isRunning = True
    isConnected = False

    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.bind(("127.0.0.1", 8222))
    mySocket.listen(5)

    my_dungeon = Dungeon.Dungeon()
    my_player = Player.Player(my_dungeon, '1-entrance')
    input_manager = Input.Input()

    my_accept_thread = threading.Thread(target=accept_clients, args=(mySocket, ))
    my_accept_thread.start()

    while isRunning == True:
        lost_clients = []

        clients_lock.acquire()
        for client in clients:
            try:
                data = client.recv(4096)
                print("Input from client: " + str(client) + ": " + data.decode("utf-8"))
                client_reply = input_manager.player_input()
                client.send(client_reply.encode())
            except socket.error:
                lost_clients.append(client)
                print("Client lost ...")

        for client in lost_clients:
            clients.pop(client)

        clients_lock.release()

        time.sleep(0.5)

        #if isConnected == False:
        #    print("Waiting for client ...")
        #    client = mySocket.accept()
#
        #try:
        #    data = client[0].recv(4096)
        #    print(data.decode("utf-8"))
        #    seqID = 0
        #    isConnected = True
        #    print("Client connected")
        #except socket.error:
        #    isConnected = False
#
        #while isConnected == True:
        #    testString = str(seqID) + ": " + time.ctime()
#
        #    try:
        #        print("Sending test string: " + testString)
        #        client[0].send(testString.encode())
        #        seqID += 1
        #        time.sleep(0.5)
        #    except socket.error:
        #        isConnected = False
        #        client = None
        #        print("Client lost")
#