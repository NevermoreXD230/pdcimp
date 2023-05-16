import socket
import pickle

# function to check if a number is prime
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

def prime_numbers(start, end, ip, port):
    results = []
    for n in range(start, end):
        if is_prime(n):
            results.append(n)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            data = pickle.dumps(results)
            conn.sendall(data)

if __name__ == '__main__':
    # define IP address and port to listen on
    ip = '192.168.83.46'
    port = 5000

    # start listening for requests
    while True:
        print(f"Listening on {ip}:{port}")
        prime_numbers(0, 0, ip, port)
