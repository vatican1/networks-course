import os
import socket
import sys

HOST = "127.0.0.1"
PORT = 2390
FILE_PATH = os.path.join(os.getcwd(), 'localfiles')

if __name__ == "__main__":
    PORT = int(sys.argv[1])

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen(1) 
print("start at", PORT)
while True:
    clientSocket, addr = serverSocket.accept()
    request = clientSocket.recv(1024).decode()

    requestedFilePath = os.path.join(FILE_PATH, request.split()[1][1:])

    if os.path.exists(os.path.join(requestedFilePath)):
        with open(requestedFilePath, 'rb') as file:
            file_content = file.read()
            print("file open")
        response = 'HTTP/1.1 200 OK\n\n'.encode() + file_content
    else:
        print("don't find file")
        response = 'HTTP/1.1 404 \n\nFile not found'.encode()

    clientSocket.sendall(response)
    clientSocket.close()
