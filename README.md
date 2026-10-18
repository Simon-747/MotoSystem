
# MotoSystem

Motorcycle Management and Maintenance System developed with Python and FastAPI.

## Description

MotoSystem is an academic software development project designed to manage motorcycle owners, motorcycles, and maintenance records through a REST API.

The application uses Pydantic for data validation and CSV files for local data storage.

## Features

- Register and list motorcycle owners.
- Retrieve, update, and delete owner records.
- Register and list motorcycles.
- Retrieve, update, and delete motorcycle records.
- Register and list maintenance records.
- Retrieve, update, and delete maintenance records.
- Validate relationships between owners, motorcycles, and maintenance records.
- Prevent deleting owners or motorcycles that have associated records.

## Technologies

- Python 3.13
- FastAPI
- Pydantic
- CSV for data storage
- Git and GitHub for version control

## Requirements

- Python 3.13 or a compatible version.
- pip package manager.
- Git.

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

If Python's virtual environment package is not installed, run:

```bash
sudo apt update
sudo apt install python3-venv
```

Then create and activate the environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

On Windows and Ubuntu, with the virtual environment activated, run:

```bash
python -m pip install --upgrade pip
pip install "fastapi[standard]" email-validator
```

## Running the Application

With the virtual environment activated, start the development server:

```bash
fastapi dev main.py
```

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## Data Storage

MotoSystem stores records locally in CSV files inside the `data/` directory.

CSV files are excluded from version control. Therefore, a fresh installation starts without existing records, and users can create new records through the API.

## Author

Academic project developed as part of a Software Development course.
