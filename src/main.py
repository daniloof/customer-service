from fastapi import FastAPI
from src.adapters.inbound.rest.customer_routes import router as customer_router
from contextlib import asynccontextmanager
from src.infrastructure.db.init_db import test_db_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    test_db_connection()

    yield

app = FastAPI(lifespan=lifespan)

app.include_router(customer_router)