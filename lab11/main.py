import socket
import struct
import time
import sys

# Создаем сокет для отправки ICMP пакетов
sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
sock.settimeout(1.0)

# Функция для вычисления контрольной суммы ICMP пакета
def checksum(data):
    checksum = 0
    num_shorts = len(data) // 2
    for i in range(num_shorts):
        short = struct.unpack('!H', data[i * 2:i * 2 + 2])[0]
        checksum += short
    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    checksum += (checksum >> 16)
    return ~checksum & 0xFFFF

# Функция для отправки ICMP запроса
def send_icmp_request(dest_addr, ttl):
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
    icmp_header = struct.pack('!BBHHH', 8, 0, 0, 0, 0)
    icmp_checksum = checksum(icmp_header)
    icmp_packet = struct.pack('!BBHHH', 8, 0, icmp_checksum, 0, 0)
    try:
        sock.sendto(icmp_packet, (dest_addr, 0))
        send_time = time.time()
        data, addr = sock.recvfrom(1024)
        recv_time = time.time()
        rtt = (recv_time - send_time) * 1000
        ip_addr = addr[0]
        print(f'{ip_addr} (RTT: {rtt:.2f} ms)')
        return ip_addr
    except socket.timeout:
        print('timeout!')
        return None

# Функция для выполнения трассировки
def traceroute(dest_addr, max_hops=30, num_packets=3):
    print(f'Traceroute to {dest_addr}:')
    for ttl in range(1, max_hops + 1):
        print(f'{ttl}.', end=' ')
        for _ in range(num_packets):
            ip_addr = send_icmp_request(dest_addr, ttl)
            if ip_addr:
                ip_addrs.add(ip_addr)
                if ip_addr == dest_addr:
                    print("\nReached destination.")
                    return
        print()

# Получаем аргументы командной строки
destination = sys.argv[1]
max_hops = 15
num_packets = int(sys.argv[2]) if len(sys.argv) > 2 else 3

ip_addrs = set()

traceroute(destination, max_hops, num_packets)
sock.close()