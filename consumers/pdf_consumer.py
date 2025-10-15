# consumers/pdf_consumer.py
import pika
import json
import sys
import time
import random

consumer_name = sys.argv[1] if len(sys.argv) > 1 else 'PDFConsumer'

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='pdf_queue', durable=True)
channel.basic_qos(prefetch_count=1)

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"[{consumer_name}] Processing PDF task: {data}")
    time.sleep(random.uniform(2, 4))  # simulate work
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"[{consumer_name}] Done with: {data}")

channel.basic_consume(queue='pdf_queue', on_message_callback=callback, auto_ack=False)
print(f"[{consumer_name}] Waiting for messages...")
channel.start_consuming()
