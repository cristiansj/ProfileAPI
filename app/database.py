from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Crea el motor de la base de datos
database_url = settings.database_url
engine = create_engine(database_url)

# Crea la sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para las clases de modelo
Base = declarative_base()