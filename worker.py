import socket

# Check if a number is prime
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

# Receive prime number from server and send result back
def verify_prime(server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('worker_ip', 5000))
        s.listen()
        conn, addr = s.accept()
        with conn:
            prime = int(conn.recv(1024).decode())
            result = is_prime(prime)
            conn.sendall(str(result).encode())

if __name__ == '__main__':
    # Set server IP and port
    server_ip = 'server_ip'
    server_port = 5000

    # Verify prime number
    verify_prime(server_ip, server_port)
