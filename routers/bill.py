from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlmodel import Session

from models.bill import (
    BillCreate,
    BillBase,
    Bill,
    BillUpdateInput,
    BillUpdate,
    BillPart,
    BillDB,
)
from models.user import UserID
from models.maintenance import MaintenanceID
from models.parts import Parts

from data.db.db_connection import get_session

from data.db.operations.bill_operation_db import (
    create_bill_db,
    read_all_bills_db,
    read_one_bill_db,
    update_bill_db,
    delete_bill_db,
)

router = APIRouter()


def validate_bill_relations(
    session: Session,
    user_id: int,
    maintenance_id: int
):
    user = session.get(UserID, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    maintenance = session.get(MaintenanceID, maintenance_id)

    if maintenance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Maintenance not found"
        )


@router.post("/", response_model=Bill, status_code=status.HTTP_201_CREATED)
def create_bill(
    new_bill: BillCreate,
    session: Session = Depends(get_session)
):
    validate_bill_relations(
        session,
        new_bill.user_id,
        new_bill.maintenance_id
    )

    bill_parts = []

    for bill_part in new_bill.parts:
        part = session.get(Parts, bill_part.part_id)

        if part is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Part with id {bill_part.part_id} not found"
            )

        if not part.is_active:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Part with id {bill_part.part_id} is inactive"
            )

        bill_parts.append(
            BillPart(
                part_id=part.id,
                quantity=bill_part.quantity,
                unit_price=part.price
            )
        )

    bill_data = BillBase(
        user_id=new_bill.user_id,
        maintenance_id=new_bill.maintenance_id,
        date=new_bill.date,
        description=new_bill.description,
        parts=bill_parts,
        labor_cost=new_bill.labor_cost
    )

    return create_bill_db(session, bill_data)


@router.get("/", response_model=list[Bill])
def read_all_bills(
    session: Session = Depends(get_session)
):
    return read_all_bills_db(session)


@router.get("/{bill_id}", response_model=Bill)
def read_one_bill(
    bill_id: int,
    session: Session = Depends(get_session)
):
    bill = read_one_bill_db(session, bill_id)

    if bill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bill not found"
        )

    return bill


@router.put("/{bill_id}", response_model=Bill)
def update_bill(
    bill_id: int,
    updated_bill: BillUpdateInput,
    session: Session = Depends(get_session)
):
    current_bill = read_one_bill_db(session, bill_id)

    if current_bill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bill not found"
        )

    updated_data = current_bill.model_dump(
        exclude={"parts_total", "total"}
    )

    new_data = updated_bill.model_dump(exclude_unset=True)

    if "parts" in new_data and new_data["parts"] is not None:
        bill_parts = []

        for bill_part in new_data["parts"]:
            part = session.get(Parts, bill_part["part_id"])

            if part is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Part with id {bill_part['part_id']} not found"
                )

            if not part.is_active:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Part with id {bill_part['part_id']} is inactive"
                )

            bill_parts.append(
                BillPart(
                    part_id=part.id,
                    quantity=bill_part["quantity"],
                    unit_price=part.price
                )
            )

        new_data["parts"] = bill_parts

    updated_data.update(new_data)

    validate_bill_relations(
        session,
        updated_data["user_id"],
        updated_data["maintenance_id"]
    )

    bill_update = BillUpdate(**updated_data)

    return update_bill_db(session, bill_id, bill_update)


@router.delete("/{bill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bill(
    bill_id: int,
    session: Session = Depends(get_session)
):
    deleted = delete_bill_db(session, bill_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bill not found"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
