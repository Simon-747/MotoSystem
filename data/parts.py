import csv
from pathlib import Path

from models.parts import PartsBase, Parts, PartsUpdate

database = Path(__file__).with_name("parts.csv")

column_fields = [
    "id",
    "name",
    "description",
    "category",
    "brand",
    "compatible_brands",
    "price",
    "stock",
]

def write_into_csv(register: Parts):
    file_exists = database.exists() and database.stat().st_size > 0

    with open(database, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_fields)

        if not file_exists:
            writer.writeheader()

        row = register.model_dump(mode="json")
        row["compatible_brands"] = ",".join(register.compatible_brands)
        writer.writerow(row)

def next_id():
    try:
        with open(database, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            max_id = max(int(row["id"]) for row in reader)
            return max_id + 1
    except (FileNotFoundError, ValueError):
        return 1

def create_parts_register(new_parts: PartsBase):
    new_id = next_id()
    new_parts_id = Parts(
        id=new_id,
        **new_parts.model_dump()
    )

    write_into_csv(new_parts_id)
    return new_parts_id

def read_all_parts_csv():
    try:
        with open(database, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            parts_list = []

            for row in reader:
                row["id"] = int(row["id"])
                row["compatible_brands"] = (
                    row["compatible_brands"].split(",")
                    if row["compatible_brands"]
                    else []
                )
                row["price"] = float(row["price"])
                row["stock"] = int(row["stock"])

                parts_list.append(Parts(**row))

            return parts_list

    except FileNotFoundError:
        return []

def read_one_parts_csv(parts_id: int):
    for parts in read_all_parts_csv():
        if parts.id == parts_id:
            return parts

    return None

def update_parts_csv(parts_id: int, updated_parts: PartsUpdate):
    parts_list = read_all_parts_csv()

    for index, parts in enumerate(parts_list):
        if parts.id == parts_id:
            updated_data = parts.model_dump()
            updated_data.update(
                updated_parts.model_dump(exclude_unset=True)
            )

            parts_list[index] = Parts(**updated_data)

            with open(database, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(
                    csvfile,
                    fieldnames=column_fields
                )
                writer.writeheader()

                for register in parts_list:
                    row = register.model_dump(mode="json")
                    row["compatible_brands"] = ",".join(
                        register.compatible_brands
                    )
                    writer.writerow(row)

            return parts_list[index]

    return None

def delete_parts_csv(parts_id: int):
    parts_list = read_all_parts_csv()
    remaining_parts = [
        parts for parts in parts_list
        if parts.id != parts_id
    ]

    if len(parts_list) == len(remaining_parts):
        return None

    with open(database, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=column_fields
        )
        writer.writeheader()

        for register in remaining_parts:
            row = register.model_dump(mode="json")
            row["compatible_brands"] = ",".join(
                register.compatible_brands
            )
            writer.writerow(row)

    return True
