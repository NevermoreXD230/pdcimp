import pika
import random
import math

def mpow(N, K, M):
    if K == 1:
        return N
    elif K % 2 == 0:
        X = mpow(N, K // 2, M)
        return (X * X) % M
    else:
        X = mpow(N, K - 1, M)
        return (X * N) % M

def fermat(P):
    if P == 1:
        return "ok"
    else:
        for _ in range(10):  # Perform the test 10 times
            R = random.randint(1, P - 1)
            T = mpow(R, P - 1, P)
            if T != 1:
                return "no"
        return "ok"

def generate_prime():
    # Code to generate a large prime number goes here.
    # You can use any algorithm of your choice.
    # For simplicity, we'll return a small prime number in this example.
    return 17

def callback(ch, method, properties, body):
    prime = int(body)
    print("Received prime number:", prime)
    result = fermat(prime)
    print("Result:", result)
    ch.basic_publish(exchange='', routing_key=properties.reply_to, body=result)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)
    print("Server started. Waiting for prime numbers...")
    channel.start_consuming()

start()
