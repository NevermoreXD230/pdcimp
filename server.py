import socket
import pickle

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

def start_server():
    # Set up the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.83.205', 5000))
    server_socket.listen()

    # Accept connections from the workers
    worker_connections = []
    for _ in range(2):
        conn, addr = server_socket.accept()
        worker_connections.append(conn)

    # Generate primes and distribute tasks to the workers
    start = 2
    end = 1000000
    chunk_size = (end - start) // len(worker_connections)
    tasks = [(start + i * chunk_size, start + (i + 1) * chunk_size) for i in range(len(worker_connections))]
    tasks[-1] = (tasks[-1][0], end)  # Adjust the last task to cover the remaining range

    for i, conn in enumerate(worker_connections):
        task = tasks[i]
        conn.sendall(pickle.dumps(task))

    # Collect results from the workers
    all_primes = []
    for conn in worker_connections:
        primes = pickle.loads(conn.recv(1024))
        all_primes.extend(primes)

    # Print the generated prime numbers
    print("Generated prime numbers:")
    for prime in all_primes:
        print(prime)

    # Close the connections
    for conn in worker_connections:
        conn.close()

if __name__ == '__main__':
    start_server()
