import random
import time
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
    num_queue = Queue()
    result_queue = Queue()
    assigned_numbers = Queue()  # Queue for assigning numbers to workers

    def worker_task(worker_id):
        while True:
            result_queue.put(worker_id)  # Signal worker availability to the server

            num = assigned_numbers.get()  # Wait for a number to test
            if num is None:
                break

            if fermat(num):
                result_queue.put((worker_id, num))  # Report prime number to server

    # Start worker processes
    workers = []
    for i in range(num_workers):
        p = Process(target=worker_task, args=(i,))
        p.start()
        workers.append(p)

    next_number = 2
    while True:
        for p in primes_found:
            if next_number % p == 0:
                break
        else:
            num_queue.put(next_number)  # Send number to the queue for testing

        # Assign numbers to available workers
        while not num_queue.empty():
            worker_id = result_queue.get()
            if worker_id is not None:
                num = num_queue.get()  # Get the number to assign to the worker
                assigned_numbers.put(num)  # Assign the number to the worker

        while not result_queue.empty():
            data = result_queue.get()
            if isinstance(data, tuple):
                worker_id, prime = data
                primes_found.append(prime)
                print(f"Worker {worker_id} found prime: {prime}")

        next_number += 1

    # Stop worker processes
    for _ in range(num_workers):
        assigned_numbers.put(None)

    for p in workers:
        p.join()

if __name__ == "__main__":
    num_workers = 2  # Adjust the number of workers as per your requirement
    server(num_workers)
