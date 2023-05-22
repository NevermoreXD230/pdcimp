import pika

credentials = pika.PlainCredentials('your_username', 'your_password')
parameters = pika.ConnectionParameters(host='192.168.74.46', credentials=credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

def mpow(n, k, m):
    if k == 1:
        return n
    if k % 2 == 0:
        x = mpow(n, k // 2, m)
        return (x * x) % m
    else:
        x = mpow(n, k - 1, m)
        return (x * n) % m

def fermat(p):
    if p == 1:
        return False
    for _ in range(5):  # Run the test 5 times for high accuracy
        r = random.randint(1, p - 1)
        t = mpow(r, p - 1, p)
        if t != 1:
            return False
    return True

def callback(ch, method, properties, body):
    number = int(body)
    result = fermat(number)
    response = "ok" if result else "no"
    ch.basic_publish(exchange='', routing_key=properties.reply_to, body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()
