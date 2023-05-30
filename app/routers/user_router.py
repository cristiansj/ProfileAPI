from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.models.user import User as UserModel
from app.models.credential import Credential as CredentialModel
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.database import SessionLocal
from app.utils.auth import get_current_user
from passlib.hash import bcrypt
import logging
from sqlalchemy.orm import joinedload
import pika
import json


logger = logging.getLogger(__name__)

router = APIRouter()


def send_message_to_rabbitmq(message, routing_key):

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel() 
    channel.exchange_declare(exchange='my_exchange', exchange_type='direct')

    if routing_key == "usr_delete":
        message_dict = {"user_id": message}
        channel.queue_declare(queue='usr_delete', durable=True, arguments={'x-queue': 'usr_delete'})
        channel.queue_bind(exchange='my_exchange', queue='usr_delete', routing_key=routing_key)
        print("Se envió a la cola usr_delete")
    
    if routing_key == "usr_update":
        channel.queue_declare(queue='usr_update', durable=True, arguments={'x-queue': 'usr_update'})
        channel.queue_bind(exchange='my_exchange', queue='usr_update', routing_key=routing_key)
        print("Se envió a la cola usr_update")

    if routing_key == "usr_create":
        # Asumiendo que el objeto 'message' en otros casos tiene un método 'to_dict()'
        message_dict = message.to_dict()
        channel.queue_declare(queue='usr_create', durable=True, arguments={'x-queue': 'usr_create'})
        channel.queue_bind(exchange='my_exchange', queue='usr_create', routing_key=routing_key)
        print("Se envió a la cola usr_create")    
    
    json_message = json.dumps(message_dict)
    channel.basic_publish(exchange='my_exchange', routing_key=routing_key, body=json_message)
    print(" [x] Sent '{}'".format(json_message))
    connection.close()




@router.post("/profile", response_model=UserResponse, responses={
    201: {"description": "Usuario creado exitosamente"},
    400: {"description": "Datos de usuario inválidos o credenciales no válidas"},
    500: {"description": "Error al crear el usuario en la base de datos o al enviar el mensaje a RabbitMQ"}
})
async def create_user(user: UserCreate):
    """
    Crea un nuevo usuario en la base de datos y envía un mensaje a la cola RabbitMQ.

    - **user**: Objeto UserCreate con los datos del nuevo usuario.
    """
    db = SessionLocal()

    try:

        hashed_password = bcrypt.hash(user.credential.password)

       # Crear la credencial y agregarla a la base de datos
        credential = CredentialModel(id=user.credential.id, username=user.credential.username, password=hashed_password, rol=user.credential.rol)
        db.add(credential)
        db.commit()
        db.refresh(credential)

        # Crear un nuevo usuario y asignarle la clave foránea credential_id
        new_user = UserModel(id=user.id, nombre=user.nombre, apellido=user.apellido, correo=user.correo, credential_id=credential.id)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Cargar la relación credential antes de cerrar la sesión
        db.refresh(new_user.credential)

        send_message_to_rabbitmq(new_user, "usr_create")

        return JSONResponse(
            status_code=201,
            content="Usuario creado exitosamente"
        )
    except Exception as e:
        logger.exception("Error al crear el usuario o al enviar el mensaje a RabbitMQ")

        raise HTTPException(status_code=500, detail="Error al crear el usuario o al enviar el mensaje a RabbitMQ")

    finally:
        db.close()
        return new_user

@router.get("/profile/{user_id}", response_model=UserResponse, responses={
    404: {"description": "Usuario no encontrado"},
    401: {"description": "No autorizado"}
})
async def get_user(user_id: str):
    """
    Obtiene un usuario por su ID.

    - **user_id**: ID del usuario a buscar.

    Retorna el usuario con el ID proporcionado.

    """

    # Obtener el usuario con el ID proporcionado
    with SessionLocal() as db:
        user = db.query(UserModel).options(joinedload(UserModel.credential)).filter(UserModel.id == user_id).first()

        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
    

@router.put("/profile/{user_id}", response_model=UserResponse, responses={
    400: {"description": "Datos de usuario inválidos o credenciales no válidas"},
    401: {"description": "No autorizado"},
    404: {"description": "Usuario no encontrado"},
    500: {"description": "Error al actualizar el usuario en la base de datos o al enviar el mensaje a RabbitMQ"}
})
async def update_user(user_id: str, updated_user: UserUpdate):
    """
    Actualiza un usuario por su ID.

    - **user_id**: ID del usuario a actualizar.
    - **updated_user**: Objeto UserUpdate con los datos actualizados del usuario.

    Actualiza el usuario con el ID proporcionado si es el mismo que el usuario actual. Si no es el mismo, retorna un mensaje de "Unauthorized".

    Ejemplos de códigos de error:
    - 400: Datos de usuario inválidos o credenciales no válidas.
    - 401: No autorizado.
    - 404: Usuario no encontrado.
    - 500: Error al actualizar el usuario en la base de datos o al enviar el mensaje a RabbitMQ.
    """

    # Actualizar el usuario con el ID proporcionado
    db = SessionLocal()
    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if user:
        try:
            user.nombre = updated_user.nombre
            user.apellido = updated_user.apellido
            user.correo = updated_user.correo
            credential = CredentialModel(id=updated_user.credential.id, username=updated_user.credential.username, password=updated_user.credential.password, rol=updated_user.credential. Grol)
            user.credential = credential
            db.commit()
            db.refresh(user)
            db.close()
            send_message_to_rabbitmq(updated_user, "usr_update")
            return update_user
        except Exception as e:
            db.close()
            raise HTTPException(status_code=500, detail="Error al actualizar el usuario en la base de datos o al enviar el mensaje a RabbitMQ")
    else:
        db.close()
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
@router.delete("/profile/{user_id}", responses={
    404: {"description": "Usuario no encontrado"},
    401: {"description": "No autorizado"}
})
async def delete_user(user_id: str):
    """
    Elimina un usuario por su ID.

    - **user_id**: ID del usuario a eliminar.
    - **current_user**: Usuario actual autenticado.

    Elimina el usuario con el ID proporcionado si es el mismo que el usuario actual. Si no es el mismo, retorna un mensaje de "Unauthorized".

    Ejemplos de códigos de error:
    - 404: Usuario no encontrado.
    - 401: No autorizado.
    """
        # Eliminar el usuario con el ID proporcionado
    db = SessionLocal()
    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if user:
        db.delete(user)
        db.commit()
        db.close()
        send_message_to_rabbitmq(user_id, "usr_delete")
        return {"message": "Usuario eliminado"}
    else:
        db.close()
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    

