from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.domain.exceptions import (CustomerNotFoundError, EmailAlreadyExistsError, InvalidZipCodeError)
from src.adapters.inbound.rest.customer_routes import router as customer_router
from contextlib import asynccontextmanager
from src.infrastructure.db.init_db import test_db_connection


app = FastAPI()

@app.exception_handler(CustomerNotFoundError)
async def customer_not_found_exception_handler(request: Request, exc: CustomerNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )

@app.exception_handler(EmailAlreadyExistsError)
async def email_already_exists_exception_handler(request: Request, exc: EmailAlreadyExistsError):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)}
    )

@app.exception_handler(InvalidZipCodeError)
async def invalid_zip_code_exception_handler(request: Request, exc: InvalidZipCodeError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

app.include_router(customer_router)