import pika

def connect_to_rabbitmq():
         
         connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
         channel = connection.channel()
         channel.queue_declare(queue='cola1')
         channel.basic_consume(queue='cola1', on_message_callback=on_message)
         channel.start_consuming()

def on_message(channel, method, properties, body):
         print("Received: {}".format(body))

         if __name__ == "__main__":
            connect_to_rabbitmq()