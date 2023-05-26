import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='cola2')

channel.basic_publish(exchange='', routing_key='cola2', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()
