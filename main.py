from fastapi import FastAPI
from routers import user, motorcycle, maintenance, mechanic, parts

app = FastAPI()

app.include_router(router=user.router, prefix= "/users", tags=["users"])
app.include_router(router=motorcycle.router, prefix="/motorcycles", tags=["motorcycles"])
app.include_router(router=maintenance.router, prefix="/maintenances", tags=["maintenances"])
app.include_router(router=mechanic.router, prefix="/mechanics", tags=["mechanics"])
app.include_router(router=parts.router, prefix="/parts", tags=["parts"])