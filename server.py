import random
import time
from multiprocessing import Process

def is_prime(n):
    if n == 1:
        return False

    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False

    return True

def generate_prime():
    while True:
        prime = random.randint(10**15, 10**16)
        if is_prime(prime):
            return prime

def worker(worker_id, worker_ip):
    while True:
        prime = generate_prime()

        print(f"Worker {worker_id} ({worker_ip}) received number: {prime}")
        pg()
        print(f"Worker {worker_id} ({worker_ip}) is verifying the number...")

        if is_prime(prime):
            print(f"Worker {worker_id} ({worker_ip}) successfully verified a prime number: {prime}")
            break
        else:
            print(f"Worker {worker_id} ({worker_ip}) found that the number is not prime.")

        fetch_numbers_from_workers(worker_ip)

def pg():
    x = random.randint(1, 100)
    y = random.randint(1, 100)
    z = x + y

def fetch_numbers_from_workers(worker_ip):
    print(f"Fetching numbers from workers at {worker_ip}...")
    delay = random.uniform(6, 7)
    start_time = time.time()
    while time.time() - start_time < delay:
        pg()

if __name__ == "__main__":
    num_workers = 2

    worker_ips = {
        0: "192.168.83.46",
        1: "192.168.83.185"
    }

    workers = []
    for i in range(num_workers):
        p = Process(target=worker, args=(i, worker_ips[i]))
        p.start()
        workers.append(p)

    for _ in range(10):
        print("Server sending a number to workers...")
        fetch_numbers_from_workers(random.choice(list(worker_ips.values())))
        print()

    for p in workers:
        p.join()

