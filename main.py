from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./contacts.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    mobile = Column(String, index=True)
    email = Column(String, index=True)
    message = Column(String)

Base.metadata.create_all(bind=engine)

class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    mobile : str
    email: str
    message: str

@app.post("/contact")
def create_contact(contact: ContactCreate):
    db = SessionLocal()
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    db.close()
    return {"status": "success", "message": "Contact form submitted successfully"}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Contact Form API"}
