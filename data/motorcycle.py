import csv
from pathlib import Path

from models.motorcycle import MotorcycleBase, MotorcycleID


database = Path(__file__).with_name("motorcycles.csv")

column_fields = [
    "id",
    "plate",
    "brand",
    "model",
    "engine_displacement",
    "year",
    "mileage",
    "user_id",
]


def write_into_csv(register: MotorcycleID):
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


def create_motorcycle_register(new_motorcycle: MotorcycleBase):
    new_id = next_id()

    new_motorcycle_id = MotorcycleID(
        id=new_id,
        **new_motorcycle.model_dump()
    )

    write_into_csv(new_motorcycle_id)
    return new_motorcycle_id


def read_all_motorcycles_csv():
    try:
        with open(database, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            motorcycles = []

            for row in reader:
                row["id"] = int(row["id"])
                row["engine_displacement"] = int(row["engine_displacement"])
                row["year"] = int(row["year"])
                row["mileage"] = int(row["mileage"])
                motorcycles.append(MotorcycleID(**row))

            return motorcycles

    except FileNotFoundError:
        return []

def read_one_motorcycle_csv(motorcycle_id: int):
    for motorcycle in read_all_motorcycles_csv():
        if motorcycle.id == motorcycle_id:
            return motorcycle

    return None

def update_motorcycle_csv(
    motorcycle_id: int,
    updated_motorcycle: MotorcycleBase
):
    motorcycles = read_all_motorcycles_csv()

    for index, motorcycle in enumerate(motorcycles):
        if motorcycle.id == motorcycle_id:
            updated_data = updated_motorcycle.model_dump()

            motorcycles[index] = MotorcycleID(
                id=motorcycle_id,
                **updated_data
            )

            with open(database, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(
                    csvfile,
                    fieldnames=column_fields
                )
                writer.writeheader()

                for register in motorcycles:
                    writer.writerow(register.model_dump(mode="json"))

            return motorcycles[index]

    return None

def delete_motorcycle_csv(motorcycle_id: int):
    motorcycles = read_all_motorcycles_csv()

    remaining_motorcycles = [
        motorcycle
        for motorcycle in motorcycles
        if motorcycle.id != motorcycle_id
    ]

    if len(motorcycles) == len(remaining_motorcycles):
        return None

    with open(database, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=column_fields
        )
        writer.writeheader()

        for register in remaining_motorcycles:
            writer.writerow(register.model_dump(mode="json"))

    return True