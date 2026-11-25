from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Form,
    File,
    UploadFile,
    Depends
)
from pydantic import EmailStr
from sqlmodel import Session, select

from enums.id_type import IdType
from models.user import UserBase, UserID, UserUpdate
from models.motorcycle import MotorcycleID
from models.bill import BillDB

from data.image_storage import save_image, delete_image
from data.db.db_connection import get_session

from data.db.operations.user_operation_db import (
    create_user_db,
    read_all_users_db,
    read_one_user_db,
    update_user_db,
    delete_user_db
)

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
    session: Session = Depends(get_session)
):
    image_path = save_image(image, "users")

    new_user = UserBase(
        first_name=first_name,
        last_name=last_name,
        id_type=id_type,
        document=document,
        phone_number=phone_number,
        email=email,
        image=image_path
    )

    return create_user_db(session, new_user)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[UserID])
def show_users(session: Session = Depends(get_session)):
    users = read_all_users_db(session)

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found"
        )

    return users


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserID)
def get_user(
    user_id: int,
    session: Session = Depends(get_session)
):
    user = read_one_user_db(session, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.patch("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserID)
def update_user(
    user_id: int,
    updated_user: UserUpdate,
    session: Session = Depends(get_session)
):
    user = update_user_db(session, user_id, updated_user)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.patch(
    "/{user_id}/image",
    status_code=status.HTTP_200_OK,
    response_model=UserID
)
def update_user_image(
    user_id: int,
    image: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    user = read_one_user_db(session, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    old_image_path = user.image
    new_image_path = save_image(image, "users")

    updated_user = update_user_db(
        session,
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
def delete_user(
    user_id: int,
    session: Session = Depends(get_session)
):
    user = read_one_user_db(session, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    motorcycle_statement = select(MotorcycleID).where(
        MotorcycleID.user_id == user_id
    )
    motorcycles = session.exec(motorcycle_statement).first()

    if motorcycles is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete user with registered motorcycles"
        )

    bill_statement = select(BillDB).where(
        BillDB.user_id == user_id
    )
    bills = session.exec(bill_statement).first()

    if bills is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete user with registered bills"
        )

    delete_user_db(session, user_id)
