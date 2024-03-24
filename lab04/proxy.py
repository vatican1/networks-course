import click
import socket
import logging
import os


CACHE_DIR = "cache"

@click.command()
@click.argument('host', required=False, default="127.0.0.1")
@click.argument('port', required=False, default=2390)
@click.option('logfile', '-l', '--logfile', required=False, default="log.txt", type=str)
def main(host, port, logfile):
    servSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servSock.bind((host, port))
    servSock.listen(5)
    print(f"Listening on port {port}")

    while True:
        clientSocket, clientAddr = servSock.accept()
        print(f'Accept client at {clientAddr}')

        try:
            clientSocket.settimeout(100)
            request = clientSocket.recv(2048)
        except (ConnectionResetError, TimeoutError, socket.timeout):
            print("Socket Error")
        finally:
            clientSocket.settimeout(None)

        if request is None:
            print(f'Client {clientAddr} send empty req')
        else:
            response = handleRequest(request)
            clientSocket.sendall(response)
            clientSocket.close()
            print(f'Client #{clientAddr} has been served')

def readWebRequest(socket, N=2048, timeout=30):
    request = bytearray()
    try:
        socket.settimeout(timeout)
        while True:
            chunk = socket.recv(N)
            request += chunk
            if len(chunk) < N:
                break
    except (ConnectionResetError, TimeoutError, socket.timeout):
        return None
    finally:
        socket.settimeout(None)
    return request

def handleRequest(request):
    if request is None:
        return "239 no website".encode()
    method, url, protocol = request.decode().split('\r\n')[0].split()

    if '/' in url[1:]:
        host, requestedUrl = url[1:].split('/', 1)
    else:
        host = url[1:]
        requestedUrl = ""

    cacheFilename = os.path.join(CACHE_DIR, request.hex()[0:30])
    if os.path.exists(cacheFilename):
        logging.info("Cache hit!")
        with open(cacheFilename, 'rb') as cacheFile:
            cachedResponse = cacheFile.read()
            return cachedResponse
    else:
        webSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #соединение с инернетом
        try:
            webSocket.connect((host, 80))
        except socket.gaierror:
            logging.info(f"{method} {url}: 239")
            return "239 no website".encode()
    
    body = ""
    if method == "POST":
        body = request.decode().split("\r\n\r\n", 1)

    webSocket.sendall(f'{method} /{requestedUrl} {protocol}\r\nHost: {host}\r\n\r\n{body}'.encode())
    response = readWebRequest(webSocket)

    if response is not None:
        statusCode = response.decode().split("\r\n", 1)[0].split(" ", 1)[1]
        logging.info(f"{method} {url}: {statusCode}")
    else:
        logging.info(f"{method} {url}: 240")
        response = "240 no response".encode()

    with open(cacheFilename, 'wb') as cacheFile:
        cacheFile.write(response)

    return response


if __name__ == "__main__":
    main()