import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.user import User

# Crea una base de datos de prueba en memoria
engine = create_engine("sqlite:///:memory:")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea todas las tablas en la base de datos de prueba
Base.metadata.create_all(bind=engine)

@pytest.fixture
def db():
    db = SessionLocal()
    yield db
    db.close()

def test_get_user(db):
    # Crea un usuario de prueba en la base de datos
    user = User(id="123", nombre="John", apellido="Doe", correo="john.doe@example.com")
    db.add(user)
    db.commit()

    # Obtiene el usuario creado
    user = db.query(User).filter(User.id == "123").first()

    assert user
    assert user.nombre == "John"
    assert user.apellido == "Doe"
    assert user.correo == "john.doe@example.com"

def test_update_user(db):
    # Crea un usuario de prueba en la base de datos
    user = User(id="123", nombre="John", apellido="Doe", correo="john.doe@example.com")
    db.add(user)
    db.commit()

    # Actualiza el usuario creado
    user = db.query(User).filter(User.id == "123").first()
    user.nombre = "Jane"
    db.commit()

    # Obtiene el usuario actualizado
    user = db.query(User).filter(User.id == "123").first()

    assert user
    assert user.nombre == "Jane"

def test_delete_user(db):
    # Crea un usuario de prueba en la base de datos
    user = User(id="123", nombre="John", apellido="Doe", correo="john.doe@example.com")
    db.add(user)
    db.commit()

    # Elimina el usuario creado
    user = db.query(User).filter(User.id == "123").first()
    db.delete(user)
    db.commit()

    # Intenta obtener el usuario eliminado
    user = db.query(User).filter(User.id == "123").first()

    assert user is None
