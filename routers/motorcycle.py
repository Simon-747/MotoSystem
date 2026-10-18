from fastapi import APIRouter, HTTPException, status

from models.motorcycle import MotorcycleBase, MotorcycleID
from data.user import read_all_users_csv
from data.motorcycle import create_motorcycle_register
from data.motorcycle import (
    create_motorcycle_register,
    read_all_motorcycles_csv,
    read_one_motorcycle_csv,
    update_motorcycle_csv,
    delete_motorcycle_csv,
)
from data.maintenance import read_all_maintenances_csv

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MotorcycleID)
def create_motorcycle(new_motorcycle: MotorcycleBase):
    owner_exists = any(
        str(user.id) == new_motorcycle.user_id
        for user in read_all_users_csv()
    )

    if not owner_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Owner not found"
        )

    return create_motorcycle_register(new_motorcycle)

@router.get(
"/",
    status_code=status.HTTP_200_OK,
    response_model=list[MotorcycleID]
)
def show_motorcycles():
    motorcycles = read_all_motorcycles_csv()

    if not motorcycles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No motorcycles found"
        )

    return motorcycles

@router.get(
    "/{motorcycle_id}",
    status_code=status.HTTP_200_OK,
    response_model=MotorcycleID
)
def get_motorcycle(motorcycle_id: int):
    motorcycle = read_one_motorcycle_csv(motorcycle_id)

    if motorcycle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Motorcycle not found"
        )

    return motorcycle


@router.put(
    "/{motorcycle_id}",
    status_code=status.HTTP_200_OK,
    response_model=MotorcycleID
)
def update_motorcycle(
    motorcycle_id: int,
    updated_motorcycle: MotorcycleBase
):
    owner_exists = any(
        str(user.id) == updated_motorcycle.user_id
        for user in read_all_users_csv()
    )

    if not owner_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Owner not found"
        )

    motorcycle = update_motorcycle_csv(
        motorcycle_id,
        updated_motorcycle
    )

    if motorcycle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Motorcycle not found"
        )

    return motorcycle


@router.delete(
    "/{motorcycle_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_motorcycle(motorcycle_id: int):
    motorcycle = read_one_motorcycle_csv(motorcycle_id)

    if motorcycle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Motorcycle not found"
        )

    maintenances = read_all_maintenances_csv()

    has_maintenances = any(
        maintenance.motorcycle_id == str(motorcycle_id)
        for maintenance in maintenances
    )

    if has_maintenances:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete motorcycle with registered maintenances"
        )

    delete_motorcycle_csv(motorcycle_id)
