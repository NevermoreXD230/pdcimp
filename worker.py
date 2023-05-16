import socket
import pickle

def start_worker():
    # Set up the worker socket
    worker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    worker_socket.connect(('192.168.83.46', 5001))

    # Receive the task from the server
    task = pickle.loads(worker_socket.recv(1024))

    # Generate primes for the task
    primes = generate_primes(task[0], task[1])

    # Send the primes back to the server
    worker_socket.sendall(pickle.dumps(primes))

    # Clean up the socket
    worker_socket.close()

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

def generate_primes(start, end):
    primes = []
    for num in range(start, end+1):
        if is_prime(num):
            primes.append(num)
    return primes

if __name__ == '__main__':
    start_worker()
