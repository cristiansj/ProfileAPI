from fastapi import FastAPI
from app.routers import auth_router, user_router

app = FastAPI()

# Registra los routers
app.include_router(auth_router.router)
app.include_router(user_router.router)