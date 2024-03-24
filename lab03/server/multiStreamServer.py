
import socket
import threading
import os
import sys

def handle_client(clientSocket):
    while True:
        request = clientSocket.recv(1024).decode()
        if request == '':
            print("break connection")
            break
        requestedFilePath = os.path.join(FILE_PATH, request.split()[1][1:])
        if os.path.exists(os.path.join(requestedFilePath)):
            with open(requestedFilePath, 'rb') as file:
                file_content = file.read()
                print("file open")
            response = 'HTTP/1.1 200 OK\n\n'.encode() + file_content
        else:
            print("don't find file")
            response = 'HTTP/1.1 404 \n\nFile not found'.encode()
        clientSocket.send(response)

    print("Client disconnect")
    clientSocket.close()
    connectionSemaphore.release() # клиент отключился - обновили



HOST = "127.0.0.1"
PORT = 2397
FILE_PATH = os.path.join(os.getcwd(), 'server')
CONC_LVL = 5

if __name__ == "__main__":
    PORT = int(sys.argv[1])
    CONC_LVL = int(sys.argv[2])

connectionSemaphore = threading.Semaphore(CONC_LVL) #так отслеживаем количество клиентов

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print("Server listening on port ", PORT)

while True:
    client_socket, addr = server_socket.accept()
    print("Connected by ", addr)
    connectionSemaphore.acquire()
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
