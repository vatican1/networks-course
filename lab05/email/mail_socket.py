import socket
import ssl
import base64

smtp_server = 'smtp.mail.ru'
smtp_port = 587

receiver_email = 'vatican2001@gmail.com'
sender_email = 'vitya-zakharov-2025@mail.ru'
password = '...' # тут пришлось создавать специальный пароль для внешних приложений

subject = 'Test Email'
message = 'Hello, this is a test email.'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((smtp_server, smtp_port))
    response = client_socket.recv(1024)
    print(1, response.decode())

    client_socket.sendall(b'HELO smtp.mail.ru\r\n')
    response = client_socket.recv(1024)
    print(2, response.decode())

    client_socket.sendall(b'STARTTLS\r\n')
    response = client_socket.recv(1024)
    print(3, response.decode())

    context = ssl.create_default_context()
    client_socket_SSL = context.wrap_socket(client_socket, server_hostname=smtp_server)

    client_socket_SSL.sendall(b'HELO smtp.mail.ru\r\n')
    response = client_socket_SSL.recv(1024)
    print(4, response.decode())

    base64_str = ("\x00"+sender_email+"\x00"+password).encode()
    base64_str = base64.b64encode(base64_str)
    authMsg = "AUTH PLAIN ".encode()+base64_str+"\r\n".encode()
    client_socket_SSL.send(authMsg)
    recv_auth = client_socket_SSL.recv(1024)
    print(5, recv_auth.decode())

    client_socket_SSL.sendall(b'MAIL FROM:<' + sender_email.encode() + b'>\r\n')
    response = client_socket_SSL.recv(1024)
    print(6, response.decode())

    client_socket_SSL.sendall(b'RCPT TO:<' + receiver_email.encode() + b'>\r\n')
    response = client_socket_SSL.recv(1024)
    print(7, response.decode())

    client_socket_SSL.sendall(b'DATA\r\n')
    response = client_socket_SSL.recv(1024)
    print(8, response.decode())

    client_socket_SSL.sendall(f'Subject: {subject}\r\n\r\n'.encode())

    client_socket_SSL.sendall(message.encode())
    client_socket_SSL.sendall(b'\r\n.\r\n')
    response = client_socket_SSL.recv(1024)
    print(9, response.decode())

    client_socket_SSL.sendall(b'QUIT\r\n')
    response = client_socket_SSL.recv(1024)
    print(10, response.decode())




