from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from routers import user, motorcycle, maintenance, parts, bill

app = FastAPI()

IMAGES_DIR = Path(__file__).resolve().parent / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

app.mount(
    "/images",
    StaticFiles(directory=IMAGES_DIR),
    name="images"
)

app.include_router(router=user.router, prefix="/users", tags=["users"])
app.include_router(router=motorcycle.router, prefix="/motorcycles", tags=["motorcycles"])
app.include_router(router=maintenance.router, prefix="/maintenances", tags=["maintenances"])
app.include_router(router=parts.router, prefix="/parts", tags=["parts"])
app.include_router(router=bill.router, prefix="/bills", tags=["bills"])