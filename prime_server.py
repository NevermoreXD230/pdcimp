import pika
import random

credentials = pika.PlainCredentials('your_username', 'your_password')
parameters = pika.ConnectionParameters(host='192.168.74.205', credentials=credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_prime():
    prime = random.randint(1000000, 9999999)
    while not is_prime(prime):
        prime += 1
    channel.basic_publish(exchange='', routing_key='task_queue', body=str(prime))
    print("Published prime number:", prime)

generate_prime()

connection.close()
