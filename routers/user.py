from fastapi import APIRouter, HTTPException, status

from models.user import UserBase, UserID, UserUpdate
from data.user import (
    create_user_register,
    read_all_users_csv,
    read_one_user_csv,
    update_user_csv,
    delete_user_csv,
)
from data.motorcycle import read_all_motorcycles_csv
from data.bill import read_all_bills_csv

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserID)
def create_user(new_user: UserBase):
    return create_user_register(new_user)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[UserID])
def show_users():
    users = read_all_users_csv()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found",
        )

    return users


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserID)
def get_user(user_id: int):
    user = read_one_user_csv(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.patch("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserID)
def update_user(user_id: int, updated_user: UserUpdate):
    user = update_user_csv(user_id, updated_user)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(user_id: int):
    user = read_one_user_csv(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    motorcycles = read_all_motorcycles_csv()

    has_motorcycles = any(
        motorcycle.user_id == str(user_id)
        for motorcycle in motorcycles
    )

    if has_motorcycles:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete user with registered motorcycles"
        )

    bills = read_all_bills_csv()

    has_bills = any(
        bill.user_id == user_id
        for bill in bills
    )

    if has_bills:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete user with registered bills"
        )

    delete_user_csv(user_id)

