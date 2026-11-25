from sqlmodel import Session, select

from models.motorcycle import MotorcycleBase, MotorcycleID


def create_motorcycle_db(
    session: Session,
    new_motorcycle: MotorcycleBase
):
    motorcycle = MotorcycleID(
        **new_motorcycle.model_dump()
    )

    session.add(motorcycle)
    session.commit()
    session.refresh(motorcycle)

    return motorcycle


def read_all_motorcycles_db(session: Session):
    statement = select(MotorcycleID)
    motorcycles = session.exec(statement).all()

    return motorcycles


def read_one_motorcycle_db(
    session: Session,
    motorcycle_id: int
):
    motorcycle = session.get(MotorcycleID, motorcycle_id)

    return motorcycle


def update_motorcycle_db(
    session: Session,
    motorcycle_id: int,
    updated_motorcycle: MotorcycleBase
):
    motorcycle = session.get(MotorcycleID, motorcycle_id)

    if motorcycle is None:
        return None

    updated_data = updated_motorcycle.model_dump()

    for key, value in updated_data.items():
        setattr(motorcycle, key, value)

    session.add(motorcycle)
    session.commit()
    session.refresh(motorcycle)

    return motorcycle


def delete_motorcycle_db(
    session: Session,
    motorcycle_id: int
):
    motorcycle = session.get(MotorcycleID, motorcycle_id)

    if motorcycle is None:
        return None

    session.delete(motorcycle)
    session.commit()

    return True
