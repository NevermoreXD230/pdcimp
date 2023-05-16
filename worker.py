import socket
import pickle

# Define a function to start a worker
def start_worker():
    # Set up the worker socket
    worker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    worker_socket.connect(('192.168.83.205', 5000))

    # Receive tasks from the server and send results back
    while True:
        task = pickle.loads(worker_socket.recv(1024))
        if task is None:
            break
        start, end = task  # Unpack the task tuple

        # Perform the computation to find prime numbers
        primes = []
        for num in range(start, end + 1):
            if is_prime(num):
                primes.append(num)

        # Send the computed primes back to the server
        worker_socket.sendall(pickle.dumps(primes))

    # Clean up the socket
    worker_socket.close()

# Helper function to check if a number is prime
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

# Start the worker
start_worker()
