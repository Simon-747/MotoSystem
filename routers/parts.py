from fastapi import APIRouter, HTTPException

from models.parts import PartsBase, Parts, PartsUpdate
from data.parts import (
    create_parts_register,
    read_all_parts_csv,
    read_one_parts_csv,
    update_parts_csv,
    delete_parts_csv,
)


router = APIRouter()


@router.post("/", response_model=Parts, status_code=201)
def create_parts(parts: PartsBase):
    return create_parts_register(parts)


@router.get("/", response_model=list[Parts])
def read_parts():
    return read_all_parts_csv()


@router.get("/{parts_id}", response_model=Parts)
def read_part(parts_id: int):
    parts = read_one_parts_csv(parts_id)

    if parts is None:
        raise HTTPException(status_code=404, detail="Part not found")

    return parts


@router.put("/{parts_id}", response_model=Parts)
def update_parts(parts_id: int, updated_parts: PartsUpdate):
    parts = update_parts_csv(parts_id, updated_parts)

    if parts is None:
        raise HTTPException(status_code=404, detail="Part not found")

    return parts


@router.delete("/{parts_id}")
def delete_parts(parts_id: int):
    deleted = delete_parts_csv(parts_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Part not found")

    return {"message": "Part deleted successfully"}
