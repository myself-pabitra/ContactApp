# app/crud.py

from sqlalchemy.orm import Session
from app.models import Contact


def create_contact(db: Session, first_name: str, last_name: str, mobile: str, email: str, message: str):
    db_contact = Contact(first_name=first_name, last_name=last_name,
                         mobile=mobile, email=email, message=message)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_contacts(db: Session):
    return db.query(Contact).all()
