from fastapi import APIRouter, Depends
from app.models.user import User as UserModel
from app.models.credential import Credential as CredentialModel
from app.schemas.user import UserCreate, UserResponse
from app.database import SessionLocal
from app.utils.auth import get_current_user
import pika
import json

router = APIRouter()

@router.post("/profile", response_model=UserResponse)
def create_user(user: UserCreate):
    db = SessionLocal()

    try:
        # Crear la credencial y agregarla a la base de datos
        credential = CredentialModel(id=user.credential.id, username=user.credential.username, password=user.credential.password, rol=user.credential.rol)
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

        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declarar la cola donde se enviará el mensaje
        channel.queue_declare(queue='nuevo_usuario')

        # Serializar el nuevo usuario a JSON
        user_json = json.dumps(new_user.__dict__)

        # Enviar el mensaje JSON a la cola
        channel.basic_publish(exchange='', routing_key='nuevo_usuario', body=user_json)

        return new_user
    finally:
        db.close()
        # Cerrar la conexión con RabbitMQ
        connection.close()

@router.get("/profile/{user_id}")
def get_user(user_id: str, current_user: UserModel = Depends(get_current_user)):
    if current_user.id == user_id:
        # Obtener el usuario con el ID proporcionado
        db = SessionLocal()
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        db.close()

        if user:
            return user
        else:
            return {"message": "User not found"}
    else:
        return {"message": "Unauthorized"}

@router.put("/profile/{user_id}", response_model=UserResponse)
def update_user(user_id: str, updated_user: UserCreate, current_user: UserModel = Depends(get_current_user)):
    if current_user.id == user_id:
        # Actualizar el usuario con el ID proporcionado
        db = SessionLocal()
        user = db.query(UserModel).filter(UserModel.id == user_id).first()

        if user:
            user.nombre = updated_user.nombre
            user.apellido = updated_user.apellido
            user.correo = updated_user.correo
            credential = CredentialModel(username=updated_user.credential.username, password=updated_user.credential.password, rol=updated_user.credential.rol)
            user.credential = credential
            db.commit()
            db.refresh(user)
            db.close()
            return user
        else:
            db.close()
            return {"message": "User not found"}
    else:
        return {"message": "Unauthorized"}

@router.delete("/profile/{user_id}")
def delete_user(user_id: str, current_user: UserModel = Depends(get_current_user)):
    if current_user.id == user_id:
        # Eliminar el usuario con el ID proporcionado
        db = SessionLocal()
        user = db.query(UserModel).filter(UserModel.id == user_id).first()

        if user:
            db.delete(user)
            db.commit()
            db.close()
            return {"message": "User deleted"}
        else:
            db.close()
            return {"message": "User not found"}
    else:
        return {"message": "Unauthorized"}
