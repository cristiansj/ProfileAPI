import pika
import json

def send_message_to_rabbitmq(message: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='cola2', arguments={'x-queue': 'cola2'})
    channel.queue_bind(exchange='', routing_key='cola2', arguments={'x-queue': 'cola2'})

    json_message = json.dumps(message)
    channel.basic_publish(exchange='', routing_key='cola2', body=json_message)
    print(" [x] Sent '{}'".format(json_message))
    connection.close()