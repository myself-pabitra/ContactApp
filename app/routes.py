# app/routes.py

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.crud import create_contact, get_contacts
from app.database import get_db

router = APIRouter()


@router.post("/contact")
def create_contact_route(request: Request, first_name=Form(...), last_name=Form(...), mobile=Form(...), email=Form(...), message=Form(...), db: Session = Depends(get_db)):
    create_contact(db, first_name, last_name, mobile, email, message)
    # return {"status": "success", "message": "Contact form submitted successfully"}


@router.get("/")
def read_root():
    return {"message": "Welcome to the Contact Form API"}


@router.get("/view-contacts", response_class=HTMLResponse)
def view_contacts(db: Session = Depends(get_db)):
    contacts = get_contacts(db)
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
    <h2>Contacts Details</h2>
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
        ''.join([
            f'''<tr><td>{contact.first_name}</td><td>{contact.last_name}</td><td>{
                contact.mobile}</td><td>{contact.email}</td><td>{contact.message}</td></tr>'''
            for contact in contacts
        ])
    }
      </tbody>
    </table>
  </body>
</html>
""")
