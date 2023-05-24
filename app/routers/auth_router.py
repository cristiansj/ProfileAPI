from fastapi import APIRouter
from app.utils.auth import authenticate_user, create_token

router = APIRouter()

@router.post("/login")
def login(username: str, password: str):
    user = authenticate_user(username, password)
    if user:
        token = create_token(user.id)
        return {"token": token}
    return {"message": "Invalid credentials"}