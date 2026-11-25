# MotoSystem

MotoSystem is a motorcycle management and maintenance system developed with Python and FastAPI. It provides tools to manage users, motorcycles, maintenance records, spare parts, and invoices through a REST API.

The project uses SQLModel and SQLite for data persistence, Pydantic for data validation, and supports image uploads for user profiles.

## Features

- **User Management:** Create, read, update, and delete users, including profile image uploads and updates.
- **Motorcycle Management:** Register, consult, update, and delete motorcycles associated with users.
- **Maintenance Management:** Record and manage motorcycle maintenance history.
- **Spare Parts Management:** Manage spare parts, including stock, prices, categories, brands, and compatible motorcycle brands.
- **Invoice Management:** Create, consult, update, and delete invoices associated with users and maintenance records.
- **Data Validation:** Validate input data and enforce business rules.
- **Database Relationships:** Maintain relationships between users, motorcycles, maintenance records, spare parts, and invoices.
- **Deletion Restrictions:** Prevent deleting records that are still referenced by related entities.
- **Invoice Calculations:** Automatically calculate parts subtotals and invoice totals.
- **Inactive Parts Validation:** Prevent inactive spare parts from being included in invoices.
- **Image Storage:** Upload and update user profile images, stored locally in the project's `images/` directory.

## Technologies Used

- **Python 3.13**
- **FastAPI:** REST API development.
- **Pydantic:** Data validation.
- **SQLModel:** SQL database models and operations.
- **SQLAlchemy:** Database engine and connection management.
- **SQLite:** Relational database.
- **StrEnum:** Enumerations for predefined values.
- **Git and GitHub:** Version control and source code management.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Simon-747/MotoSystem.git
cd MotoSystem
```

### 2. Create and activate a virtual environment

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Ubuntu / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

Upgrade pip and install the project dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Running the Application

Start the development server with:

```bash
fastapi dev main.py
```

Once the server is running, the API documentation is available at:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Database and Image Storage

MotoSystem uses SQLite as its database engine, with SQLModel and SQLAlchemy for database management.

- The database is stored locally at `data/db/motosystem.db`.
- Database tables are created automatically when the application starts.
- User profile images are stored locally in the project's `images/` directory and served through the `/images` route.
- The previous CSV implementation is preserved in `data/csv/` for reference. CSV files are no longer used for active data persistence.

The database and uploaded images are local application data and are not included in the Git repository.

## Version Control

GitHub repository:
[https://github.com/Simon-747/MotoSystem](https://github.com/Simon-747/MotoSystem)

## Author

**Simón Raúl Rodríguez Velosa**
