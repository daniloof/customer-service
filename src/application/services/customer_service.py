from sqlalchemy.orm import Session
from src.adapters.outbound.db.customer_repository import (create_customer as repo_create_customer,
                                                          get_customers as repo_get_customers)

def create_customer(db:Session, name:str, email:str):
    return repo_create_customer(db, name, email)

def get_customer(db: Session):
    return repo_get_customers(db)