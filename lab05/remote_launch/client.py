import socket
import click


IP = "127.0.0.1"
PORT = 8008
programm_call = 'ping yandex.ru'
def run_client():
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rid = 0
    client_sock.connect((IP, PORT))

    while True:
        request = programm_call
        client_sock.sendall(request.encode())
        response = bytearray()
        try:
            while True:
                chunk = client_sock.recv(1024)
                response += chunk
                if len(chunk) < 1024:
                    break
        except ConnectionResetError:
            return None
        print(response.decode("UTF-8"))


if __name__ == '__main__':
    run_client()