import socket
import pickle
import time
import multiprocessing

# function to check if a number is prime
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

def prime_numbers(start, end):
    return [n for n in range(start, end) if is_prime(n)]

def divide_range(num_workers, range_start, range_end):
    range_size = range_end - range_start
    chunk_size = range_size // num_workers
    ranges = []
    for i in range(num_workers):
        chunk_start = range_start + i*chunk_size
        if i < num_workers-1:
            chunk_end = chunk_start + chunk_size
        else:
            chunk_end = range_end
        ranges.append((chunk_start, chunk_end))
    return ranges

if __name__ == '__main__':
    # define IP addresses and ports of the workers
    workers = [
        ('192.168.83.46', 5000),
        ('192.168.83.185', 5000)
    ]

    # define range of numbers to search for primes
    start = 1000000000
    end = 1000100000

    # divide range into chunks for each worker
    ranges = divide_range(len(workers), start, end)

    # create a process for each worker
    processes = []
    for i, (ip, port) in enumerate(workers):
        p = multiprocessing.Process(target=prime_numbers, args=(ranges[i][0], ranges[i][1], ip, port))
        processes.append(p)
        p.start()

    # wait for all processes to finish
    for p in processes:
        p.join()

    # combine results from all workers
    results = []
    for ip, port in workers:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            data = s.recv(1024)
            results.extend(pickle.loads(data))

    # print the number of prime numbers found
    print(f"{len(results)} prime numbers found in range {start} to {end}")
