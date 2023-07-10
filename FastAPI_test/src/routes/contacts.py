from typing import List
from datetime import date

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactModel
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts')


@router.get("/")
async def list_contacts(skip: int = 0, limit: int = 30, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(skip, limit, db)
    return contacts


@router.get("/find")
async def find(first_name: str | None = None, last_name: str | None = None, email: str | None = None, db: Session = Depends(get_db)):
    contacts = await repository_contacts.find_contacts(first_name, last_name, email, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")
    return contacts


@router.get("/congratulate")
async def birthdays_per_week(db: Session = Depends(get_db)):
    contacts = await repository_contacts.congratulate(db)
    return contacts


@router.get("/{contact_id}")
async def contact_info(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/")
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, db)


@router.put("/{contact_id}")
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}")
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/find")
async def find(first_name=None, last_name=None, email=None, db: Session = Depends(get_db)):
    print('I in find')
    contacts = await repository_contacts.find_contacts(first_name, last_name, email, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")
    return contacts


