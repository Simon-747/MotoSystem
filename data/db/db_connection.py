from pathlib import Path

from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy import event

from models.user import UserID
from models.motorcycle import MotorcycleID
from models.maintenance import MaintenanceID
from models.parts import Parts
from models.bill import BillDB, BillPartDB


DATABASE_PATH = Path(__file__).resolve().parent / "motosystem.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


@event.listens_for(engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def create_db_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
