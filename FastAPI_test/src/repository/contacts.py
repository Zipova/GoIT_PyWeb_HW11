from typing import List
from datetime import date, datetime

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactModel, db: Session) -> Contact:
    if body.birthday:
        body.birthday = datetime.strptime(body.birthday, '%d-%m-%Y').date()
    contact = Contact(first_name=body.first_name, last_name=body.last_name, email=body.email, phone=body.phone, birthday=body.birthday)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = datetime.strptime(body.birthday, '%d-%m-%Y').date()
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session)  -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def find_contacts(first_name, last_name, email, db: Session) -> List[Contact] | None:
    if first_name:
        return db.query(Contact).filter(Contact.first_name == first_name).all()
    if last_name:
        return db.query(Contact).filter(Contact.last_name == last_name).all()
    if email:
        return db.query(Contact).filter(Contact.email == email).all()
    return None


async def congratulate(db: Session):
    current = date.today()
    contacts = db.query(Contact).all()
    result = []
    for contact in contacts:
        if contact.birthday:
            bd_this_year = date(day=contact.birthday.day, month=contact.birthday.month, year=current.year)
            delta = bd_this_year - current
            if delta.days in range(0, 8):
                result.append(contact)
    return result

