import csv
import json
from pathlib import Path

from models.bill import BillBase, Bill, BillUpdate

database = Path(__file__).with_name("bill.csv")

column_fields = [
    "id",
    "user_id",
    "maintenance_id",
    "date",
    "description",
    "parts",
    "labor_cost",
]


def bill_to_row(register: Bill) -> dict:
    row = register.model_dump(
        mode="json",
        exclude={"parts_total", "total"}
    )
    row["parts"] = json.dumps(row["parts"], ensure_ascii=False)
    return row


def write_into_csv(register: Bill):
    file_exists = database.exists() and database.stat().st_size > 0

    with open(database, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_fields)

        if not file_exists:
            writer.writeheader()

        writer.writerow(bill_to_row(register))


def next_id():
    try:
        with open(database, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            max_id = max(int(row["id"]) for row in reader)
            return max_id + 1
    except (FileNotFoundError, ValueError):
        return 1


def create_bill_register(new_bill: BillBase):
    new_id = next_id()

    new_bill_id = Bill(
        id=new_id,
        **new_bill.model_dump()
    )

    write_into_csv(new_bill_id)
    return new_bill_id


def read_all_bills_csv():
    try:
        with open(database, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            bills_list = []

            for row in reader:
                row["id"] = int(row["id"])
                row["user_id"] = int(row["user_id"])
                row["maintenance_id"] = int(row["maintenance_id"])
                row["parts"] = json.loads(row["parts"])
                row["labor_cost"] = float(row["labor_cost"])

                bills_list.append(Bill(**row))

            return bills_list

    except FileNotFoundError:
        return []


def read_one_bill_csv(bill_id: int):
    for bill in read_all_bills_csv():
        if bill.id == bill_id:
            return bill

    return None


def update_bill_csv(bill_id: int, updated_bill: BillUpdate):
    bills_list = read_all_bills_csv()

    for index, bill in enumerate(bills_list):
        if bill.id == bill_id:
            updated_data = bill.model_dump(
                exclude={"parts_total", "total"}
            )

            updated_data.update(
                updated_bill.model_dump(exclude_unset=True)
            )

            bills_list[index] = Bill(**updated_data)

            with open(database, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(
                    csvfile,
                    fieldnames=column_fields
                )
                writer.writeheader()

                for register in bills_list:
                    writer.writerow(bill_to_row(register))

            return bills_list[index]

    return None


def delete_bill_csv(bill_id: int):
    bills_list = read_all_bills_csv()

    remaining_bills = [
        bill for bill in bills_list
        if bill.id != bill_id
    ]

    if len(bills_list) == len(remaining_bills):
        return None

    with open(database, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=column_fields
        )
        writer.writeheader()

        for register in remaining_bills:
            writer.writerow(bill_to_row(register))

    return True
