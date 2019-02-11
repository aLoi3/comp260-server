import socket
import time
import Input

if __name__ == '__main__':

    isConnected = False
    mySocket = None
    isRunning = True

    input_manager = Input.Input(mySocket)

    while isRunning:
        while not isConnected:

            if mySocket is None:
                mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                mySocket.connect(("127.0.0.1", 8222))
                isConnected = True
            except socket.error:
                isConnected = False

            if isConnected:
                try:
                    testString = "Connected ..."
                    mySocket.send(testString.encode())
                except:
                    isConnected = False
                    mySocket = None
                    print("No server")
                    time.sleep(1.0)

        while isConnected:
            try:
                input_manager.player_input(mySocket)
                time.sleep(0.5)
                #data = mySocket.recv(4096)
                #print(data.decode("utf-8"))
            except:
                isConnected = False
                mySocket = None
