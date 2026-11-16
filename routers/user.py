from fastapi import APIRouter, HTTPException, status, Form, File, UploadFile
from pydantic import EmailStr

from enums.id_type import IdType
from models.user import UserBase, UserID, UserUpdate
from data.image_storage import save_image, delete_image

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
def create_user(
    first_name: str = Form(...),
    last_name: str = Form(...),
    id_type: IdType = Form(...),
    document: str = Form(...),
    phone_number: str = Form(...),
    email: EmailStr = Form(...),
    image: UploadFile = File(...),
):
    image_path = save_image(image, "users")

    new_user = UserBase(
        first_name=first_name,
        last_name=last_name,
        id_type=id_type,
        document=document,
        phone_number=phone_number,
        email=email,
        image=image_path,
    )

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


@router.patch(
    "/{user_id}/image",
    status_code=status.HTTP_200_OK,
    response_model=UserID
)
def update_user_image(user_id: int, image: UploadFile = File(...)):
    user = read_one_user_csv(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    old_image_path = user.image

    new_image_path = save_image(image, "users")

    updated_user = update_user_csv(
        user_id,
        UserUpdate(image=new_image_path)
    )

    if updated_user is None:
        delete_image(new_image_path)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    delete_image(old_image_path)

    return updated_user


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

