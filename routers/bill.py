from fastapi import APIRouter, HTTPException, Response, status

from models.bill import BillBase, Bill, BillUpdate
from data.bill import (
    create_bill_register,
    read_all_bills_csv,
    read_one_bill_csv,
    update_bill_csv,
    delete_bill_csv,
)

router = APIRouter()


@router.post("/", response_model=Bill, status_code=status.HTTP_201_CREATED)
def create_bill(new_bill: BillBase):
    return create_bill_register(new_bill)


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
def update_bill(bill_id: int, updated_bill: BillUpdate):
    bill = update_bill_csv(bill_id, updated_bill)

    if bill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bill not found"
        )

    return bill


@router.delete("/{bill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bill(bill_id: int):
    deleted = delete_bill_csv(bill_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bill not found"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
