from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User
from app.models.credential import Credential
from typing import Optional
from sqlalchemy.orm import Session
from app.database import SessionLocal, Base
from app.config import settings

ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

def get_user_by_id(user_id: str, db: Session) -> Optional[User]:
    query = db.query(User).filter(User.id == user_id)
    result = query.first()
    if result:
        return result
    return None

# En algún lugar de tu código donde quieras utilizar la función get_user_by_id()
db = SessionLocal()
user = get_user_by_id("some_user_id", db)
db.close()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_token(user_id: str) -> str:
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": datetime.utcnow() + expires_delta, "sub": user_id}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(username: str, password: str, db: Session) -> Optional[User]:
    # Consulta el usuario y las credenciales relacionadas en base al nombre de usuario proporcionado
    query = db.query(User, Credential).filter(User.credential_id == Credential.id).filter(Credential.username == username)
    result = query.first()

    if result:
        user, credential = result

        # Verifica si la contraseña proporcionada coincide con la contraseña almacenada
        if verify_password(password, credential.password):
            return user

    # Si no se encuentra el usuario o la contraseña no coincide, devuelve None
    return None

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    if user_id == "123":
        return User(id="123", nombre="Test", apellido="User", correo="testuser@example.com")

    raise credentials_exception
