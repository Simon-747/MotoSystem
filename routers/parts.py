from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session, select
from sqlalchemy import func, or_

from models.parts import PartsBase, Parts, PartsUpdate

from data.db.db_connection import get_session

from data.db.operations.parts_operation_db import (
    create_parts_db,
    read_one_parts_db,
    update_parts_db,
    delete_parts_db,
)

router = APIRouter()


@router.post("/", response_model=Parts, status_code=status.HTTP_201_CREATED)
def create_parts(
    parts: PartsBase,
    session: Session = Depends(get_session)
):
    return create_parts_db(session, parts)


@router.get("/", response_model=list[Parts])
def read_parts(
    search: str | None = None,
    category: str | None = None,
    is_active: bool | None = None,
    session: Session = Depends(get_session)
):
    statement = select(Parts)

    if search is not None:
        search_term = search.lower()
        statement = statement.where(
            or_(
                func.lower(Parts.name).contains(search_term),
                func.lower(Parts.brand).contains(search_term)
            )
        )

    if category is not None:
        statement = statement.where(
            func.lower(Parts.category) == category.lower()
        )

    if is_active is not None:
        statement = statement.where(Parts.is_active == is_active)

    parts_list = session.exec(statement).all()
    return parts_list


@router.get("/{parts_id}", response_model=Parts)
def read_part(
    parts_id: int,
    session: Session = Depends(get_session)
):
    parts = read_one_parts_db(session, parts_id)

    if parts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Part not found"
        )

    return parts


@router.put("/{parts_id}", response_model=Parts)
def update_parts(
    parts_id: int,
    updated_parts: PartsUpdate,
    session: Session = Depends(get_session)
):
    parts = update_parts_db(session, parts_id, updated_parts)

    if parts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Part not found"
        )

    return parts


@router.delete("/{parts_id}")
def delete_parts(
    parts_id: int,
    session: Session = Depends(get_session)
):
    deleted = delete_parts_db(session, parts_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Part not found"
        )

    return {"message": "Part deleted successfully"}
