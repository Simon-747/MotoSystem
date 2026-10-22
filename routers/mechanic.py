from fastapi import APIRouter, HTTPException

from models.mechanic import MechanicBase, Mechanic, MechanicUpdate
from data.mechanic import (
    create_mechanic_register,
    read_all_mechanics_csv,
    read_one_mechanic_csv,
    update_mechanic_csv,
    delete_mechanic_csv,
)

router = APIRouter()

@router.post("/", response_model=Mechanic, status_code=201)
def create_mechanic(mechanic: MechanicBase):
    return create_mechanic_register(mechanic)

@router.get("/", response_model=list[Mechanic])
def read_mechanics():
    return read_all_mechanics_csv()

@router.get("/{mechanic_id}", response_model=Mechanic)
def read_mechanic(mechanic_id: int):
    mechanic = read_one_mechanic_csv(mechanic_id)

    if mechanic is None:
        raise HTTPException(status_code=404, detail="Mechanic not found")

    return mechanic

@router.put("/{mechanic_id}", response_model=Mechanic)
def update_mechanic(mechanic_id: int, updated_mechanic: MechanicUpdate):
    mechanic = update_mechanic_csv(mechanic_id, updated_mechanic)

    if mechanic is None:
        raise HTTPException(status_code=404, detail="Mechanic not found")

    return mechanic

@router.delete("/{mechanic_id}")
def delete_mechanic(mechanic_id: int):
    deleted = delete_mechanic_csv(mechanic_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Mechanic not found")

    return {"message": "Mechanic deleted successfully"}
