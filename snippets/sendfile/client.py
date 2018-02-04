import socket

CHUNK_SIZE = 8 * 1024

sock = socket.socket()
sock.connect(('localhost', 12345))
chunk = sock.recv(CHUNK_SIZE)
while chunk:
    chunk = sock.recv(CHUNK_SIZE)
sock.close()