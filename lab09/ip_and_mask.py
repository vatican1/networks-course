import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.connect(('8.8.8.8', 80))
ip_address = s.getsockname()[0]
s.close()

print(f"IP-адрес: {ip_address}")

subnet_mask = socket.inet_ntoa(socket.inet_aton(ip_address)[::-1].lstrip(b'\xff'))
print(f"Маска сети: {subnet_mask}")