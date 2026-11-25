import csv
from pathlib import Path

from models.maintenance import MaintenanceBase, MaintenanceID


database = Path(__file__).with_name("maintenances.csv")

column_fields = [
    "id",
    "motorcycle_id",
    "maintenance_type",
    "date",
    "mileage",
    "description",
    "cost",
]


def write_into_csv(register: MaintenanceID):
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


def create_maintenance_register(new_maintenance: MaintenanceBase):
    new_id = next_id()

    new_maintenance_id = MaintenanceID(
        id=new_id,
        **new_maintenance.model_dump()
    )

    write_into_csv(new_maintenance_id)
    return new_maintenance_id

def read_all_maintenances_csv():
    try:
        with open(database, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            maintenances = []

            for row in reader:
                row["id"] = int(row["id"])
                row["mileage"] = int(row["mileage"])
                row["cost"] = float(row["cost"])
                maintenances.append(MaintenanceID(**row))

            return maintenances

    except FileNotFoundError:
        return []

def read_one_maintenance_csv(maintenance_id: int):
    for maintenance in read_all_maintenances_csv():
        if maintenance.id == maintenance_id:
            return maintenance

    return None

def update_maintenance_csv(
    maintenance_id: int,
    updated_maintenance: MaintenanceBase
):
    maintenances = read_all_maintenances_csv()

    for index, maintenance in enumerate(maintenances):
        if maintenance.id == maintenance_id:
            updated_data = updated_maintenance.model_dump()

            maintenances[index] = MaintenanceID(
                id=maintenance_id,
                **updated_data
            )

            with open(database, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(
                    csvfile,
                    fieldnames=column_fields
                )
                writer.writeheader()

                for register in maintenances:
                    writer.writerow(register.model_dump(mode="json"))

            return maintenances[index]

    return None

def delete_maintenance_csv(maintenance_id: int):
    maintenances = read_all_maintenances_csv()

    remaining_maintenances = [
        maintenance
        for maintenance in maintenances
        if maintenance.id != maintenance_id
    ]

    if len(maintenances) == len(remaining_maintenances):
        return None

    with open(database, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=column_fields
        )
        writer.writeheader()

        for register in remaining_maintenances:
            writer.writerow(register.model_dump(mode="json"))

    return True