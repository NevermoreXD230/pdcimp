import random
from multiprocessing import Process, Queue

def fermat(n):
    if n == 1:
        return True

    for _ in range(10):  # Perform the test multiple times
        r = random.randint(1, n-1)
        if pow(r, n-1, n) != 1:
            return False

    return True

def server(num_workers):
    primes_found = []

    def worker_task(worker_id, num_queue, result_queue):
        while True:
            num = num_queue.get()  # Wait for a number to test
            if num is None:
                break

            if fermat(num):
                result_queue.put((worker_id, num))  # Report prime number to server

    num_queue = Queue()
    result_queue = Queue()

    # Start worker processes
    workers = []
    for i in range(num_workers):
        p = Process(target=worker_task, args=(i, num_queue, result_queue))
        p.start()
        workers.append(p)

    next_number = 2
    while True:
        for p in primes_found:
            if next_number % p == 0:
                break
        else:
            num_queue.put(next_number)  # Send number to a worker for testing

        while not result_queue.empty():
            worker_id, prime = result_queue.get()
            primes_found.append(prime)
            print(f"Worker {worker_id} found prime: {prime}")

        next_number += 1

    # Stop worker processes
    for _ in range(num_workers):
        num_queue.put(None)

    for p in workers:
        p.join()

if __name__ == "__main__":
    num_workers = 2  # Adjust the number of workers as per your requirement
    server(num_workers)
