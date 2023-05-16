import random

def fermat(n):
    if n == 1:
        return True

    for _ in range(10):  # Perform the test multiple times
        r = random.randint(1, n-1)
        if pow(r, n-1, n) != 1:
            return False

    return True

def worker(server_address):
    while True:
        # Receive number from the server for testing
        num = int(input("Enter number to test (or -1 to exit): "))
        if num == -1:
            break

        if fermat(num):
            print(f"{num} is a prime number.")
        else:
            print(f"{num} is not a prime number.")

if __name__ == "__main__":
    server_address = "192.168.83.205"  # Update with the server's address
    worker(server_address)
