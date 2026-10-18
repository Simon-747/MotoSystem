import csv
from pathlib import Path

from models.user import UserBase, UserID, UserUpdate


database = Path(__file__).with_name("users.csv")

column_fields = [
    "id",
    "first_name",
    "last_name",
    "id_type",
    "document",
    "phone_number",
    "email",
]


def write_into_csv(register: UserID):
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


def create_user_register(new_user: UserBase):
    new_id = next_id()
    new_user_id = UserID(
        id=new_id,
        **new_user.model_dump(mode="json")
    )

    write_into_csv(new_user_id)
    return new_user_id


def read_all_users_csv():
    try:
        with open(database, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            users = []

            for row in reader:
                row["id"] = int(row["id"])
                row["id_type"] = int(row["id_type"])
                users.append(UserID(**row))

            return users

    except FileNotFoundError:
        return []


def read_one_user_csv(user_id: int):
    for user in read_all_users_csv():
        if user.id == user_id:
            return user

    return None


def update_user_csv(user_id: int, updated_user: UserUpdate):
    users = read_all_users_csv()

    for index, user in enumerate(users):
        if user.id == user_id:
            updated_data = user.model_dump()
            updated_data.update(
                updated_user.model_dump(exclude_unset=True)
            )
            users[index] = UserID(**updated_data)

            with open(database, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(
                    csvfile,
                    fieldnames=column_fields
                )
                writer.writeheader()

                for register in users:
                    writer.writerow(register.model_dump(mode="json"))

            return users[index]

    return None


def delete_user_csv(user_id: int):
    users = read_all_users_csv()
    remaining_users = [
        user for user in users if user.id != user_id
    ]

    if len(users) == len(remaining_users):
        return None

    with open(database, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=column_fields
        )
        writer.writeheader()

        for register in remaining_users:
            writer.writerow(register.model_dump(mode="json"))

    return True
