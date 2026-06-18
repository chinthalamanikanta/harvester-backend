from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.machine import router as machine_router
from app.routers.booking import router as booking_router
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(
    title="Harvester Connect API"
)
os.makedirs("uploads", exist_ok=True)

app.include_router(auth_router)
app.include_router(machine_router)
app.include_router(booking_router)
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

@app.get("/")
def home():
    return {
        "message": "Harvester Connect API Running"
    }