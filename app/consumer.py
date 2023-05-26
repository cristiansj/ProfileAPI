import pika
import pickle
import json

def callback(ch, method, properties, body):
    print(f" [x] Received {body}")

def pedido(ch, method, properties, body):
    pedido_json = body.decode('utf-8')
    pedido = json.loads(pedido_json)
    print("Pedido recibido:", pedido)

connection_params = pika.ConnectionParameters(host='localhost')
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

queue_name = 'cola3'
channel.queue_declare(queue=queue_name, durable=True)

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()