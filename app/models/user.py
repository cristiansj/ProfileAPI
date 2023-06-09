from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    correo = Column(String, unique=True)
    credential_id = Column(String, ForeignKey("credentials.id"))

    credential = relationship("Credential", backref="users")

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "correo": self.correo,
            "credential_id": self.credential_id,
        }
