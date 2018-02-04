import socket

CHUNK_SIZE = 8 * 1024

server_socket = socket.socket()
server_socket.bind(('localhost', 12345))
server_socket.listen(5)
while True:
    client_socket, addr = server_socket.accept()
    with open('4GB.bin', 'rb') as f:
        data = f.read(CHUNK_SIZE)
        while data:
            client_socket.send(data)
            data = f.read(CHUNK_SIZE)
    client_socket.close()
