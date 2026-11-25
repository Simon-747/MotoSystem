from sqlmodel import Session, select

from models.user import UserBase, UserID, UserUpdate


def create_user_db(session: Session, new_user: UserBase):
    user = UserID(
        **new_user.model_dump()
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def read_all_users_db(session: Session):
    statement = select(UserID)
    users = session.exec(statement).all()

    return users


def read_one_user_db(session: Session, user_id: int):
    user = session.get(UserID, user_id)

    return user


def update_user_db(
    session: Session,
    user_id: int,
    updated_user: UserUpdate
):
    user = session.get(UserID, user_id)

    if user is None:
        return None

    updated_data = updated_user.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def delete_user_db(session: Session, user_id: int):
    user = session.get(UserID, user_id)

    if user is None:
        return None

    session.delete(user)
    session.commit()

    return True
