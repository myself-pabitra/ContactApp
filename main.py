from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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

@app.get("/view-contacts")
def view_contacts():
    db = SessionLocal()
    contacts = db.query(Contact).all()
    db.close()
    return HTMLResponse(f"""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Contact Details</title>
    <style>
      table {{
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
      }}

      td,
      th {{
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
      }}

      tr:nth-child(even) {{
        background-color: #dddddd;
      }}
    </style>
  </head>
  <body>
    <h2>Contacts Deatails</h2>

    <table>
      <thead>
        <th>First Name</th>
        <th>Last Name</th>
        <th>Mobile</th>
        <th>Email</th>
        <th>Message</th>
      </thead>
      <tbody>
        {
          "".join([
            f"<tr><td>{contact.first_name}</td><td>{contact.last_name}</td><td>{contact.mobile}</td><td>{contact.email}</td><td>{contact.message}</td></tr>"
            for contact in contacts
          ])
        }
      </tbody>
    </table>
  </body>
</html>
"""
)
