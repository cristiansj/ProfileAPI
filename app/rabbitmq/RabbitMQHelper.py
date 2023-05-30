import pika

class RabbitMQHelper:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
    
    def declare_queues(self, queues):
        for queue in queues:
            self.channel.queue_declare(queue=queue)
    
    def send_message(self, queue, message):
        self.channel.basic_publish(exchange='',
                                   routing_key=queue,
                                   body=message)
    
    def receive_message(self, queue):
        method, properties, body = self.channel.basic_get(queue=queue, auto_ack=True)
        if method is not None:
            return body.decode('utf-8')
        else:
            return None
    
    def close_connection(self):
        self.connection.close()
