from sqlalchemy import Column, String, Enum
from app.database import Base

class Credential(Base):
    __tablename__ = "credentials"

    id = Column(String, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    rol = Column(Enum("cliente", "empleado", "administrador"))

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "rol": self.rol,
        }
