from fastapi import FastAPI
from src.adapters.inbound.rest.custimer_routes import router

app = FastAPI()

app.include_router(router)