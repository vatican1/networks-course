import socket

from funcs import package_lost

host = "127.0.0.1"
port = 8008
file_path = "receive.txt"
buff_size = 16


def run_server():
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv_sock.bind((host, port))
    print("Сервер запущен")

    f = open(file_path, "wb")
    while True:
        data, adress = serv_sock.recvfrom(buff_size)
        if package_lost():
            print("Пакет потерян")
            continue
        ack_num = int(data[0])
        data = data[1:]
        print(f"Получен пакет с ack_num {ack_num}")
        f.write(data)
        datagram = ack_num.to_bytes(1, "big") 
        serv_sock.sendto(datagram , adress)
        if ack_num == 2:
                break
            
    f.close()
    print(f"Файл {file_path} записан")

if __name__ == "__main__":
     run_server()