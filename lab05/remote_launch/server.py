import socket
import subprocess
import time

HOST = "127.0.0.1"
PORT = 8008

def handle_request(request):
    program_call = request.split()
    prog_name = program_call[0]

    proc = subprocess.Popen(program_call, stdout=subprocess.PIPE)

    response = ""
    start_time = time.monotonic()
    time_limit = 5.0

    while True:
        output = proc.stdout.readline()
        if time.monotonic() - start_time >= time_limit:
            response += "EXIT: process execution time exceeded."
            proc.kill()
            break
        else:
            if not output:
                break
            response += output.decode("utf-8")
    proc.kill()
    return response.encode()


if __name__ == "__main__":
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((HOST, PORT))
    serverSocket.listen(1) 
    print("start at", PORT)
    while True:
        clientSocket, addr = serverSocket.accept()
        request = clientSocket.recv(1024).decode()


        response = handle_request(request)

        clientSocket.sendall(response)
        clientSocket.close()