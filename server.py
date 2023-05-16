import random
import socket

# Generate a large prime number
def generate_prime():
    p = random.randint(10**10, 10**11)
    while not is_prime(p):
        p += 1
    return p

# Check if a number is prime
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

# Send prime number to worker
def send_prime(prime, worker_ip, worker_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((worker_ip, worker_port))
        s.sendall(str(prime).encode())

# Collect results from workers
def collect_results(worker_ips, worker_ports):
    results = []
    for i in range(len(worker_ips)):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((worker_ips[i], worker_ports[i]))
            s.listen()
            conn, addr = s.accept()
            with conn:
                result = conn.recv(1024).decode()
                results.append(result)
    return results

if __name__ == '__main__':
    # Set worker IPs and ports
    worker_ips = ['worker1_ip', 'worker2_ip']
    worker_ports = [5000, 5000]

    # Generate prime number
    prime = generate_prime()

    # Send prime number to workers
    for i in range(len(worker_ips)):
        send_prime(prime, worker_ips[i], worker_ports[i])

    # Collect results from workers
    results = collect_results(worker_ips, worker_ports)

    # Output final result
    if all(result == 'True' for result in results):
        print('The generated number is a prime number')
    else:
        print('The generated number is not a prime number')
