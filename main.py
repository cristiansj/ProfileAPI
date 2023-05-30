import asyncio
from fastapi import FastAPI
from app.routers.routers import router
import pika

# Importar las funciones necesarias desde el archivo consumer.py
#from app.consumer import callback, pedido, connection_params, queue_name

app = FastAPI()
app.include_router(router)

# Crear la función start_consumer para conectar y consumir mensajes de RabbitMQ
'''async def start_consumer():
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, channel.start_consuming)

# Llamar a la función start_consumer en la función main
start_consumer()'''
