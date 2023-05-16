import random
from multiprocessing import Process

def fermat(n):
    if n == 1:
        return True

    for _ in range(10):
        r = random.randint(1, n-1)
        if pow(r, n-1, n) != 1:
            return False

    return True

def generate_primes():
    
    for _ in range(10**7):
        _ = random.random()  

def worker(worker_id, worker_ip):
    num = random.randint(10**15, 10**16)
    prime = fermat(num)

    print(f"Worker {worker_id} ({worker_ip}) received number: {num}")
    generate_primes()

    if prime:
        print(f"Worker {worker_id} ({worker_ip}) successfully verified a potential prime number: {num}")

if __name__ == "__main__":
    num_workers = 2

    worker_ips = {
        0: "192.168.83.46",
        1: "192.168.83.185"
    }

    print("Starting prime number verification process...")
    print(f"Number of workers: {num_workers}\n")

    workers = []
    for i in range(num_workers):
        p = Process(target=worker, args=(i, worker_ips[i]))
        p.start()
        workers.append(p)

    for p in workers:
        p.join()

    print("\nPrime number verification process completed.")
