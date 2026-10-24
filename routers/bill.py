from fastapi import APIRouter, HTTPException, Response, status

from models.bill import (
    BillCreate,
    BillBase,
    Bill,
    BillUpdateInput,
    BillUpdate,
    BillPart,
)

from data.bill import (
    create_bill_register,
    read_all_bills_csv,
    read_one_bill_csv,
    update_bill_csv,
    delete_bill_csv,
)
from data.user import read_one_user_csv
from data.maintenance import read_one_maintenance_csv
from data.parts import read_all_parts_csv

router = APIRouter()


def validate_bill_relations(user_id: int, maintenance_id: int):
    user = read_one_user_csv(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    maintenance = read_one_maintenance_csv(maintenance_id)

    if maintenance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Maintenance not found"
        )


@router.post("/", response_model=Bill, status_code=status.HTTP_201_CREATED)
def create_bill(new_bill: BillCreate):
    validate_bill_relations(
        new_bill.user_id,
        new_bill.maintenance_id
    )

    catalog_parts = read_all_parts_csv()
    bill_parts = []

    for bill_part in new_bill.parts:
        part = next(
            (
                catalog_part
                for catalog_part in catalog_parts
                if catalog_part.id == bill_part.part_id
            ),
            None
        )

        if part is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Part with id {bill_part.part_id} not found"
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

    return create_bill_register(bill_data)


@router.get("/", response_model=list[Bill])
def read_all_bills():
    return read_all_bills_csv()


@router.get("/{bill_id}", response_model=Bill)
def read_one_bill(bill_id: int):
    bill = read_one_bill_csv(bill_id)

    if bill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bill not found"
        )

    return bill


@router.put("/{bill_id}", response_model=Bill)
def update_bill(bill_id: int, updated_bill: BillUpdateInput):
    current_bill = read_one_bill_csv(bill_id)

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
        catalog_parts = read_all_parts_csv()
        bill_parts = []

        for bill_part in new_data["parts"]:
            part = next(
                (
                    catalog_part
                    for catalog_part in catalog_parts
                    if catalog_part.id == bill_part["part_id"]
                ),
                None
            )

            if part is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Part with id {bill_part['part_id']} not found"
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
        updated_data["user_id"],
        updated_data["maintenance_id"]
    )

    bill_update = BillUpdate(**updated_data)

    return update_bill_csv(bill_id, bill_update)


@router.delete("/{bill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bill(bill_id: int):
    deleted = delete_bill_csv(bill_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bill not found"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
