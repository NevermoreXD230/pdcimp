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

def worker(worker_id, server_address):
    result_queue = Queue()

    def server_task():
        while True:
            # Signal worker availability to the server
            result_queue.put(worker_id)

            data = result_queue.get()  # Wait for server response
            if data is None:
                break

            num = data
            if fermat(num):
                result_queue.put((worker_id, num))  # Report prime number to server

    server_task_process = Process(target=server_task)
    server_task_process.start()

    while True:
        # Wait for server to assign a number
        data = result_queue.get()
        if data == worker_id:  # Ignore the worker's own signal
            continue
        elif data is None:
            break

        num = data
        if fermat(num
        if fermat(num):
            print(f"Worker {worker_id} found prime: {num}")

    server_task_process.join()

if __name__ == "__main__":
    worker_id = 1  # Update with the worker's ID
    server_address = "192.168.83.205"  # Update with the server's address
    worker(worker_id, server_address)
