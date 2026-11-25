from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session, select

from models.maintenance import MaintenanceBase, MaintenanceID
from models.motorcycle import MotorcycleID
from models.bill import BillDB

from data.db.db_connection import get_session

from data.db.operations.maintenance_operation_db import (
    create_maintenance_db,
    read_all_maintenances_db,
    read_one_maintenance_db,
    update_maintenance_db,
    delete_maintenance_db
)

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=MaintenanceID
)
def create_maintenance(
    new_maintenance: MaintenanceBase,
    session: Session = Depends(get_session)
):
    motorcycle = session.get(
        MotorcycleID,
        new_maintenance.motorcycle_id
    )

    if motorcycle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Motorcycle not found"
        )

    return create_maintenance_db(session, new_maintenance)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[MaintenanceID]
)
def show_maintenances(session: Session = Depends(get_session)):
    maintenances = read_all_maintenances_db(session)

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
def get_maintenance(
    maintenance_id: int,
    session: Session = Depends(get_session)
):
    maintenance = read_one_maintenance_db(session, maintenance_id)

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
    updated_maintenance: MaintenanceBase,
    session: Session = Depends(get_session)
):
    motorcycle = session.get(
        MotorcycleID,
        updated_maintenance.motorcycle_id
    )

    if motorcycle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Motorcycle not found"
        )

    maintenance = update_maintenance_db(
        session,
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
def delete_maintenance(
    maintenance_id: int,
    session: Session = Depends(get_session)
):
    maintenance = read_one_maintenance_db(
        session,
        maintenance_id
    )

    if maintenance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Maintenance not found"
        )

    bill_statement = select(BillDB).where(
        BillDB.maintenance_id == maintenance_id
    )
    bills = session.exec(bill_statement).first()

    if bills is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete maintenance with registered bills"
        )

    delete_maintenance_db(session, maintenance_id)
