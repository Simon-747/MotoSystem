from sqlmodel import Session, select
from models.parts import PartsBase, Parts, PartsUpdate


def create_parts_db(session: Session, new_parts: PartsBase):
    parts = Parts(**new_parts.model_dump())

    session.add(parts)
    session.commit()
    session.refresh(parts)

    return parts


def read_all_parts_db(session: Session):
    statement = select(Parts)
    parts_list = session.exec(statement).all()

    return parts_list


def read_one_parts_db(session: Session, parts_id: int):
    parts = session.get(Parts, parts_id)

    return parts


def update_parts_db(
    session: Session,
    parts_id: int,
    updated_parts: PartsUpdate
):
    parts = session.get(Parts, parts_id)

    if parts is None:
        return None

    updated_data = updated_parts.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        setattr(parts, key, value)

    session.add(parts)
    session.commit()
    session.refresh(parts)

    return parts


def delete_parts_db(session: Session, parts_id: int):
    parts = session.get(Parts, parts_id)

    if parts is None or not parts.is_active:
        return None

    parts.is_active = False

    session.add(parts)
    session.commit()
    session.refresh(parts)

    return True
