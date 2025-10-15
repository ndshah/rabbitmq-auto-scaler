# producer.py
import pika
import json
import time
import random

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='email_queue', durable=True)
channel.queue_declare(queue='pdf_queue', durable=True)

# Send 20 email tasks
for i in range(1, 21):
    msg = {'task_id': i, 'type': 'email', 'content': f"Email content {i}"}
    channel.basic_publish(
        exchange='',
        routing_key='email_queue',
        body=json.dumps(msg),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print(f"Sent email task: {msg}")

# Send 20 PDF tasks
for i in range(1, 21):
    msg = {'task_id': i, 'type': 'pdf', 'content': f"PDF content {i}"}
    channel.basic_publish(
        exchange='',
        routing_key='pdf_queue',
        body=json.dumps(msg),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print(f"Sent PDF task: {msg}")

connection.close()
