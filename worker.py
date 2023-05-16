import socket
import pickle

# Define a function to send a task to the server and receive the result
def send_task(start, end):
    # Set up the worker socket
    worker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    worker_socket.connect(('192.168.83.205', 5000))

    # Send the task to the server and receive the result
    task = (start, end)
    worker_socket.sendall(pickle.dumps(task))
    result = pickle.loads(worker_socket.recv(1024))

    # Clean up the socket
    worker_socket.close()

    return result

# Send tasks to the server and receive results
if __name__ == '__main__':
    print(send_task(2, 100))
