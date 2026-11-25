from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import user, motorcycle, maintenance, parts, bill
from data.db.db_connection import create_db_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_tables()
    yield


app = FastAPI(lifespan=lifespan)

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
