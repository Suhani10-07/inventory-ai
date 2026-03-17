from fastapi import FastAPI
from app.routes.inventory import router as inventory_router
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

app.include_router(inventory_router)