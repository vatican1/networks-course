import socket

ip_address = "127.0.0.1"

open_ports = []

for port in range(1, 10001):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)
    if s.connect_ex((ip_address, port)) == 0:
        open_ports.append(port)
    s.close()
print(f"Доступные порты {ip_address}:", open_ports)
