from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session, select

from models.motorcycle import MotorcycleBase, MotorcycleID
from models.user import UserID
from models.maintenance import MaintenanceID

from data.db.db_connection import get_session

from data.db.operations.motorcycle_operation_db import (
    create_motorcycle_db,
    read_all_motorcycles_db,
    read_one_motorcycle_db,
    update_motorcycle_db,
    delete_motorcycle_db
)

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MotorcycleID)
def create_motorcycle(
    new_motorcycle: MotorcycleBase,
    session: Session = Depends(get_session)
):
    owner = session.get(UserID, new_motorcycle.user_id)

    if owner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Owner not found"
        )

    return create_motorcycle_db(session, new_motorcycle)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[MotorcycleID]
)
def show_motorcycles(session: Session = Depends(get_session)):
    motorcycles = read_all_motorcycles_db(session)

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
def get_motorcycle(
    motorcycle_id: int,
    session: Session = Depends(get_session)
):
    motorcycle = read_one_motorcycle_db(session, motorcycle_id)

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
    updated_motorcycle: MotorcycleBase,
    session: Session = Depends(get_session)
):
    owner = session.get(UserID, updated_motorcycle.user_id)

    if owner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Owner not found"
        )

    motorcycle = update_motorcycle_db(
        session,
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
def delete_motorcycle(
    motorcycle_id: int,
    session: Session = Depends(get_session)
):
    motorcycle = read_one_motorcycle_db(session, motorcycle_id)

    if motorcycle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Motorcycle not found"
        )

    maintenance_statement = select(MaintenanceID).where(
        MaintenanceID.motorcycle_id == motorcycle_id
    )
    maintenances = session.exec(maintenance_statement).first()

    if maintenances is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete motorcycle with registered maintenances"
        )

    delete_motorcycle_db(session, motorcycle_id)
