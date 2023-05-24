from pydantic import BaseModel
from typing import List

class CredentialBase(BaseModel):
    id: str
    username: str
    password: str
    rol: str

class CredentialCreate(CredentialBase):
    pass

class Credential(CredentialBase):
    id: str

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    id: str
    nombre: str
    apellido: str
    correo: str

class UserCreate(UserBase):
    credential: CredentialCreate

class User(UserBase):
    id: str
    credential: Credential

    class Config:
        orm_mode = True

class UserResponse(User):
    pass
