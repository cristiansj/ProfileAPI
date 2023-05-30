from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.auth import authenticate_user, create_token
from app.database import SessionLocal
from app.models.user import User
from pydantic import BaseModel
from passlib.hash import bcrypt

router = APIRouter()

class LoginInput(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    token: str
@router.post("/login", response_model=TokenResponse, responses={
    401: {
        "description": "Retorna este código si el usuario no ingresó credenciales correctas",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "detail": {"type": "string"}
                    }
                }
            }
        }
    }
})
async def login(username: str, password: str):
    with SessionLocal() as db:
        user = authenticate_user(username, password, db)
    if user:
        token = create_token(user.id)
        return {"token": token}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWWW-Authenticate": "Bearer"},
        )