import matplotlib.pyplot as plt
import seaborn as sns

def benchmark():
    sock = socket.socket()
    sock.connect(('localhost', 12345))
    chunk = sock.recv(CHUNK_SIZE)
    while chunk:
        chunk = sock.recv(CHUNK_SIZE)
    sock.close()

no_sendfile_times = [timeit.timeit(benchmark, number=1) for i in range(100)]
sendfile_times = [timeit.timeit(benchmark, number=1) for i in range(100)]

sns.distplot(no_sendfile_times, label='no sendfile')
sns.distplot(sendfile_times, label='sendfile')
plt.xlim(0, 4)
plt.xlabel('execution time [s]')
plt.legend()
plt.show()
