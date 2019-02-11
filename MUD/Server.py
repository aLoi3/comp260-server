import socket
import time

if __name__ == '__main__':

    isRunning = True
    isConnected = False

    seqID = 0

    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.bind(("127.0.0.1", 8222))
    mySocket.listen(5)

    while isRunning == True:
        if isConnected == False:
            print("Waiting for client ...")
            client = mySocket.accept()

        try:
            data = client[0].recv(4096)
            print(data.encode("utf-8"))
            seqID = 0
            isConnected = True
            print("Client connected")
        except socket.error:
            isConnected = False

        while isConnected == True:
            testString = str(seqID) + ": " + time.ctime()

            try:
                print("Sending test string: " + testString)
                client[0].send(testString.encode())
                seqID += 1
                time.sleep(0.5)
            except socket.error:
                isConnected = False
                client = None
                print("Client lost")
