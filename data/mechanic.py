import csv
from pathlib import Path

from models.mechanic import MechanicBase, Mechanic, MechanicUpdate


database = Path(__file__).with_name("mechanics.csv")

column_fields = [
    "id",
    "first_name",
    "last_name",
    "document",
    "phone_number",
    "email",
]

def write_into_csv(register: Mechanic):
    file_exists = database.exists() and database.stat().st_size > 0

    with open(database, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_fields)

        if not file_exists:
            writer.writeheader()

        writer.writerow(register.model_dump(mode="json"))

def next_id():
    try:
        with open(database, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            max_id = max(int(row["id"]) for row in reader)
            return max_id + 1
    except (FileNotFoundError, ValueError):
        return 1

def create_mechanic_register(new_mechanic: MechanicBase):
    new_id = next_id()
    new_mechanic_id = Mechanic(
        id=new_id,
        **new_mechanic.model_dump(mode="json")
    )

    write_into_csv(new_mechanic_id)
    return new_mechanic_id

def read_all_mechanics_csv():
    try:
        with open(database, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            mechanics = []

            for row in reader:
                row["id"] = int(row["id"])
                mechanics.append(Mechanic(**row))

            return mechanics

    except FileNotFoundError:
        return []

def read_one_mechanic_csv(mechanic_id: int):
    for mechanic in read_all_mechanics_csv():
        if mechanic.id == mechanic_id:
            return mechanic

    return None

def update_mechanic_csv(mechanic_id: int, updated_mechanic: MechanicUpdate):
    mechanics = read_all_mechanics_csv()

    for index, mechanic in enumerate(mechanics):
        if mechanic.id == mechanic_id:
            updated_data = mechanic.model_dump()
            updated_data.update(
                updated_mechanic.model_dump(exclude_unset=True)
            )
            mechanics[index] = Mechanic(**updated_data)

            with open(database, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(
                    csvfile,
                    fieldnames=column_fields
                )
                writer.writeheader()

                for register in mechanics:
                    writer.writerow(register.model_dump(mode="json"))

            return mechanics[index]

    return None

def delete_mechanic_csv(mechanic_id: int):
    mechanics = read_all_mechanics_csv()
    remaining_mechanics = [
        mechanic for mechanic in mechanics
        if mechanic.id != mechanic_id
    ]

    if len(mechanics) == len(remaining_mechanics):
        return None

    with open(database, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=column_fields
        )
        writer.writeheader()

        for register in remaining_mechanics:
            writer.writerow(register.model_dump(mode="json"))

    return True
