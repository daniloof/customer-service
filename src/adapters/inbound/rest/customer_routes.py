from fastapi import APIRouter
from src.application.services.customer_service import create_customer

router = APIRouter()

@router.post("/customers")
def create_customer_route(data:dict):
    customer = create_customer(
        name=data["name"],
        email=data["email"]
    )

    return{
        "id":str(customer.id),
        "name":customer.name,
        "email": customer.email
    }

@router.get("/health")
def health():
    return{"status": "OK"}