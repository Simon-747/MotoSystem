from sqlmodel import Session, select

from models.maintenance import MaintenanceBase, MaintenanceID


def create_maintenance_db(
    session: Session,
    new_maintenance: MaintenanceBase
):
    maintenance = MaintenanceID(
        **new_maintenance.model_dump()
    )

    session.add(maintenance)
    session.commit()
    session.refresh(maintenance)

    return maintenance


def read_all_maintenances_db(session: Session):
    statement = select(MaintenanceID)
    maintenances = session.exec(statement).all()

    return maintenances


def read_one_maintenance_db(
    session: Session,
    maintenance_id: int
):
    maintenance = session.get(MaintenanceID, maintenance_id)

    return maintenance


def update_maintenance_db(
    session: Session,
    maintenance_id: int,
    updated_maintenance: MaintenanceBase
):
    maintenance = session.get(MaintenanceID, maintenance_id)

    if maintenance is None:
        return None

    updated_data = updated_maintenance.model_dump()

    for key, value in updated_data.items():
        setattr(maintenance, key, value)

    session.add(maintenance)
    session.commit()
    session.refresh(maintenance)

    return maintenance


def delete_maintenance_db(
    session: Session,
    maintenance_id: int
):
    maintenance = session.get(MaintenanceID, maintenance_id)

    if maintenance is None:
        return None

    session.delete(maintenance)
    session.commit()

    return True
