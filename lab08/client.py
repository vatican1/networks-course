import socket
import time
import os


from funcs import package_lost

server_ip = "127.0.0.1";
server_port = 8008
client_ip = "127.0.0.1"
client_port = 8009
file_name = "send.txt"
buff_size = 16
timeout = 1

LOCAL_STORAGE_PATH = os.getcwd()


def str_to_chunks(data: str, chunk_size=1024):
    chunk_size = min(chunk_size, len(data))
    chunks = []
    for pos in range(0, len(data),  chunk_size):
        chunks.append(data[pos:pos+chunk_size])
    return chunks


def receive_response(client_sock, buff_size=1024):
    response = bytearray()
    try:
        while True:
            chunk = client_sock.recv(buff_size)
            response += chunk
            if len(chunk) < buff_size:
                return response
    except ConnectionResetError:
        return None


def run_client():
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_sock.bind((client_ip, client_port))
    client_sock.settimeout(timeout)

    print(f"LOCAL_STORAGE_PATH {LOCAL_STORAGE_PATH}")
    if os.path.isfile(os.path.join(LOCAL_STORAGE_PATH, file_name)):
        file_path = os.path.join(LOCAL_STORAGE_PATH, file_name)

    f = open(file_path, "rb")
    chunks = str_to_chunks(f.read(), buff_size - 1)
    f.close()

    ack_num = 0
    losted_count = 0
    for chunk_num, chunk in enumerate(chunks):
        while True:
            print(f"pkg:{chunk_num}:ack_num:{ack_num}: отправляю пакет")
            if package_lost():
                print(f"pkg:{chunk_num}:ack:{ack_num}: пакет потерян")
                time.sleep(2)
                losted_count += 1
                continue

            if chunk_num == len(chunks) - 1:
                ack_num = 2

            try:
                datagram = ack_num.to_bytes(1, "big") + chunk
                client_sock.sendto(datagram, (server_ip, server_port))
                print(f"pkg:{chunk_num}:ack:{ack_num}: пакет отправлен")
                response = receive_response(client_sock, buff_size)
                response_ack_num = int(response[0])

                if (response_ack_num != ack_num):
                    print(f"pkg:{chunk_num}:ack_num:{ack_num}: неверный ack_num")
                    continue

                print(f"pkg:{chunk_num}:ack:{ack_num}: пакет передан успешно")
                ack_num = 1 - ack_num
                break

            except socket.timeout:
                print(f"pkg:{chunk_num}:ack:{ack_num}: TIMEOUT: сервер не ответил, отправляем пакет ещё раз")

    print(f"Передача файла закончена\n"
          f"Утеряно пакетов: {losted_count} из {chunk_num+1+losted_count}\n")



if __name__ == '__main__':
    run_client()