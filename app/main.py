# app/main.py

from fastapi import FastAPI
from app.routes import router as contact_router
from app.database import init_db

# Initialize the database
init_db()

app = FastAPI()

app.include_router(contact_router)
