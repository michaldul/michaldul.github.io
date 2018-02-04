---
published: true
title: File transfer over sockets without user-space memory in Python 3.5
categories: [Python]
---

Few specific design choices put Apache Kafka in the forefront of the fast messeging systems. One of them is use of 'zero-copy' mechanism. The original [paper](http://notes.stephenholiday.com/Kafka.pdf) on Kafka describes it as follows:

> A typical approach to sending bytes from a local file to a remote socket involves the following steps: (1) read data from the storage media to the page cache in an OS, (2) copy data in the page cache to an application buffer, (3) copy application buffer to another kernel buffer, (4) send the kernel buffer to the socket. This includes 4 data copying and 2 system calls. On Linux and other Unix operating systems, there exists a sendfile API [5] that can directly transfer bytes from a file channel to a socket channel. This typically avoids 2 of the copies and 1 system call introduced in steps (2) and (3).

Since Python 3.3 `sendfile` system call is available as [`os.sendfile`](https://docs.python.org/3/library/os.html#os.sendfile). Python 3.5 brings even higher-level wrapper for socket-based application [`socket.socket.sendfile`](https://docs.python.org/3/library/socket.html#socket.socket.sendfile). Let's create an example of client-server file transfer and improve it later with sendfile.

### Client-server example

```python
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
```

```python
import socket

CHUNK_SIZE = 8 * 1024

sock = socket.socket()
sock.connect(('localhost', 12345))
chunk = sock.recv(CHUNK_SIZE)
while chunk:
    chunk = sock.recv(CHUNK_SIZE)
sock.close()
```

Client does not spill on disk in purpose - we want to benchmark it and `write` operation would be the most expensive one.
Introducing `socket.socket.sendfile` call simplifies the sever code:

```python
import socket

server_socket = socket.socket()
server_socket.bind(('localhost', 12345))
server_socket.listen(5)
while True:
    client_socket, addr = server_socket.accept()
    with open('4GB.bin', 'rb') as f:
        client_socket.sendfile(f, 0)
    client_socket.close()
```

### Benchmark
Let's see how much faster this zero copy approach is. `4GB.bin` file mentioned in the listening is generated with the following bash command:
```sh
dd if=/dev/urandom of=4GB.bin bs=64M count=64 iflag=fullblock
```

I've run the client script against both servers 100 times. Distribution of execution times presents as follows:

![benchmark](/assets/images/sendfile_benchmark.png){: .align-center}


[`socket.socket.sendfile`](https://docs.python.org/3/library/socket.html#socket.socket.sendfile) approach is more than twice as fast and much more **stable** in terms of execution time. Standard deviations of times are respectively 0.68s and 0.03s.