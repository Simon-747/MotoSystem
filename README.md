# MotoSystem V.1

Motorcycle management and maintenance system developed with Python and FastAPI.

## Description

MotoSystem is an academic software development project designed to manage motorcycle owners, motorcycles, maintenance records, spare parts, and invoices through FastAPI.

The application uses Pydantic for data validation and CSV files for local data storage. It also includes predefined catalogs for identification document types and motorcycle maintenance types.

## Features

- Create, retrieve, list, update, and delete motorcycle owners.
- Create, retrieve, list, update, and delete motorcycles.
- Create, retrieve, list, update, and delete maintenance records.
- Create, retrieve, list, update, and logically delete spare parts.
- Search for spare parts by name or brand.
- Filter spare parts by category and active or inactive status.
- Create, retrieve, list, update, and delete invoices.
- Validate relationships between owners, motorcycles, maintenance records, spare parts, and invoices.
- Validate identification document types and maintenance types using predefined catalogs.
- Prevent the deletion of owners who have associated motorcycles or invoices.
- Prevent the deletion of motorcycles that have associated maintenance records.
- Prevent the deletion of maintenance records associated with invoices.
- Prevent inactive spare parts from being used when creating or updating invoices.
- Calculate invoice totals based on spare part prices and labor costs.

## Technologies Used

- Python 3.13
- FastAPI
- Pydantic
- StrEnum for predefined catalogs
- CSV files for local data storage
- Git and GitHub for version control

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Simon-747/MotoSystem.git
cd MotoSystem
```

### 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Ubuntu:**

If the package required to create virtual environments is not installed, run:

```bash
sudo apt update
sudo apt install python3-venv
```

Then, create and activate the virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

With the virtual environment activated, run:

```bash
python -m pip install --upgrade pip
pip install "fastapi[standard]" email-validator
```

## Running the Application

With the virtual environment activated, start the development server using:

```bash
fastapi dev main.py
```

## API Documentation

Once the server is running, you can access the interactive API documentation:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Version Control

The project uses Git and GitHub for version control.

Repository: [https://github.com/Simon-747/MotoSystem](https://github.com/Simon-747/MotoSystem)

## Author

Simón Raúl Rodríguez Velosa
