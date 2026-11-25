from sqlmodel import Session, select

from models.bill import (
    BillBase,
    Bill,
    BillUpdate,
    BillPart,
    BillDB,
    BillPartDB
)


def build_bill_response(session: Session, bill_db: BillDB):
    statement = select(BillPartDB).where(
        BillPartDB.bill_id == bill_db.id
    )
    parts_db = session.exec(statement).all()

    parts = [
        BillPart(
            part_id=part.part_id,
            quantity=part.quantity,
            unit_price=part.unit_price
        )
        for part in parts_db
    ]

    return Bill(
        id=bill_db.id,
        user_id=bill_db.user_id,
        maintenance_id=bill_db.maintenance_id,
        date=bill_db.date,
        description=bill_db.description,
        parts=parts,
        labor_cost=bill_db.labor_cost
    )


def create_bill_db(session: Session, new_bill: BillBase):
    bill = BillDB(
        user_id=new_bill.user_id,
        maintenance_id=new_bill.maintenance_id,
        date=new_bill.date,
        description=new_bill.description,
        labor_cost=new_bill.labor_cost
    )

    session.add(bill)
    session.flush()

    for part in new_bill.parts:
        bill_part = BillPartDB(
            bill_id=bill.id,
            part_id=part.part_id,
            quantity=part.quantity,
            unit_price=part.unit_price
        )
        session.add(bill_part)

    session.commit()
    session.refresh(bill)

    return build_bill_response(session, bill)


def read_all_bills_db(session: Session):
    statement = select(BillDB)
    bills_db = session.exec(statement).all()

    return [
        build_bill_response(session, bill)
        for bill in bills_db
    ]


def read_one_bill_db(session: Session, bill_id: int):
    bill = session.get(BillDB, bill_id)

    if bill is None:
        return None

    return build_bill_response(session, bill)


def update_bill_db(
    session: Session,
    bill_id: int,
    updated_bill: BillUpdate
):
    bill = session.get(BillDB, bill_id)

    if bill is None:
        return None

    updated_data = updated_bill.model_dump(exclude_unset=True)
    updated_parts = updated_data.pop("parts", None)

    for key, value in updated_data.items():
        setattr(bill, key, value)

    if updated_parts is not None:
        statement = select(BillPartDB).where(
            BillPartDB.bill_id == bill_id
        )
        existing_parts = session.exec(statement).all()

        for part in existing_parts:
            session.delete(part)

        for part in updated_parts:
            bill_part = BillPartDB(
                bill_id=bill_id,
                part_id=part["part_id"],
                quantity=part["quantity"],
                unit_price=part["unit_price"]
            )
            session.add(bill_part)

    session.add(bill)
    session.commit()
    session.refresh(bill)

    return build_bill_response(session, bill)


def delete_bill_db(session: Session, bill_id: int):
    bill = session.get(BillDB, bill_id)

    if bill is None:
        return None

    statement = select(BillPartDB).where(
        BillPartDB.bill_id == bill_id
    )
    existing_parts = session.exec(statement).all()

    for part in existing_parts:
        session.delete(part)

    session.delete(bill)
    session.commit()

    return True
