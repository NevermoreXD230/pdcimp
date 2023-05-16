import socket
import pickle
from multiprocessing import Process, Queue

# Define a function to check if a number is prime
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

# Define a function to handle a connection from a worker
def handle_connection(conn, queue):
    while True:
        task = conn.recv(1024)
        if not task:
            break
        start, end = task
        primes = []
        for n in range(start, end+1):
            if is_prime(n):
                primes.append(n)
        queue.put(primes)
    conn.close()

# Define a function to start the server
def start_server():
    # Set up the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('192.168.83.205', 5000))
    server_socket.listen()

    # Create a queue to store the results from the workers
    results_queue = Queue()

    # Start two worker processes
    workers = []
    for i in range(2):
        p = Process(target=start_worker, args=(results_queue,))
        p.start()
        workers.append(p)

    # Listen for connections from the workers
    while True:
        conn, addr = server_socket.accept()
        p = Process(target=handle_connection, args=(conn, results_queue))
        p.start()

    # Wait for the worker processes to finish
    for p in workers:
        p.join()

# Define a function to start a worker
def start_worker(queue):
    # Set up the worker socket
    worker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    worker_socket.connect(('192.168.83.205', 5000))

    # Send tasks to the server and receive results
    while True:
        task = queue.get()
        if task is None:
            break
        worker_socket.sendall(pickle.dumps(task))
        result = pickle.loads(worker_socket.recv(1024))
        print(result)

    # Clean up the socket
    worker_socket.close()

# Start the server
if __name__ == '__main__':
    start_server()
