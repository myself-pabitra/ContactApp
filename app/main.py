# app/main.py

from fastapi import FastAPI
from app.routes import router as contact_router
from app.database import engine
from app.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(contact_router)
