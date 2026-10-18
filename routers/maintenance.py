from fastapi import APIRouter, HTTPException, status

from models.maintenance import MaintenanceBase, MaintenanceID
from data.motorcycle import read_all_motorcycles_csv
from data.maintenance import (
    create_maintenance_register,
    read_all_maintenances_csv,
    read_one_maintenance_csv,
    update_maintenance_csv,
    delete_maintenance_csv,
)
from data.motorcycle import read_all_motorcycles_csv

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=MaintenanceID
)
def create_maintenance(new_maintenance: MaintenanceBase):
    motorcycle_exists = any(
        str(motorcycle.id) == new_maintenance.motorcycle_id
        for motorcycle in read_all_motorcycles_csv()
    )

    if not motorcycle_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Motorcycle not found"
        )

    return create_maintenance_register(new_maintenance)

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[MaintenanceID]
)
def show_maintenances():
    maintenances = read_all_maintenances_csv()

    if not maintenances:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No maintenances found"
        )

    return maintenances

@router.get(
    "/{maintenance_id}",
    status_code=status.HTTP_200_OK,
    response_model=MaintenanceID
)
def get_maintenance(maintenance_id: int):
    maintenance = read_one_maintenance_csv(maintenance_id)

    if maintenance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Maintenance not found"
        )

    return maintenance


@router.put(
    "/{maintenance_id}",
    status_code=status.HTTP_200_OK,
    response_model=MaintenanceID
)
def update_maintenance(
    maintenance_id: int,
    updated_maintenance: MaintenanceBase
):
    motorcycle_exists = any(
        str(motorcycle.id) == updated_maintenance.motorcycle_id
        for motorcycle in read_all_motorcycles_csv()
    )

    if not motorcycle_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Motorcycle not found"
        )

    maintenance = update_maintenance_csv(
        maintenance_id,
        updated_maintenance
    )

    if maintenance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Maintenance not found"
        )

    return maintenance


@router.delete(
    "/{maintenance_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_maintenance(maintenance_id: int):
    deleted = delete_maintenance_csv(maintenance_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Maintenance not found"
        )