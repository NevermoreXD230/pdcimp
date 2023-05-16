# Define a function to start a worker
def start_worker(queue):
    # Set up the worker socket
    worker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    worker_socket.connect(('192.168.83.205', 5000))

    # Send tasks to the server and receive results
    while True:
        task = queue.get()
        if task is None:
            break
        start, end = task  # Unpack the task tuple
        worker_socket.sendall(pickle.dumps(task))
        result = pickle.loads(worker_socket.recv(1024))
        print(result)

    # Clean up the socket
    worker_socket.close()

# Modify the main block to send a sentinel value to stop the workers
if __name__ == '__main__':
    queue = Queue()

    # Add tasks to the queue
    queue.put((2, 100))
    queue.put((101, 200))

    # Add sentinel values to stop the workers
    for _ in range(2):
        queue.put(None)

    # Start the workers
    workers = []
    for _ in range(2):
        p = Process(target=start_worker, args=(queue,))
        p.start()
        workers.append(p)

    # Wait for the worker processes to finish
    for p in workers:
        p.join()
