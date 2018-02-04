import socket

server_socket = socket.socket()
server_socket.bind(('localhost', 12345))
server_socket.listen(5)
while True:
    client_socket, addr = server_socket.accept()
    with open('4GB.bin', 'rb') as f:
        client_socket.sendfile(f, 0)
    client_socket.close()
