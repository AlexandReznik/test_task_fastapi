
# FastAPI Receipt Management System

## Project Setup

### Prerequisites

- Python 3.8+
- PostgreSQL (or another database that SQLAlchemy supports)

### Clone the repository

```bash
git clone https://github.com/AlexandReznik/test_task_fastapi.git
cd test_task_fastapi
```

### Install Dependencies

It’s recommended to set up a virtual environment for managing dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

### Setup Database

Make sure your PostgreSQL instance is running, and configure the database URL in the `.env` file:

```
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### Run Migrations

Run the database migrations to set up the schema:

```bash
alembic upgrade head
```

### Run the Application

To run the application locally, use the following command:

```bash
uvicorn app.main:app --reload
```

The app will be available at http://127.0.0.1:8000 or use http://127.0.0.1:8000/docs for documentation in OpenApi format.

## API Endpoints

### User Management

#### Register a New User

*POST /users/sign-up/*

Request Body:

```json
{
  "username": "test_user",
  "login": "test_login",
  "password": "testpassword"
}
```

Response:

```json
{
  "id": 1,
  "username": "test_user",
  "login": "test_login"
}
```

#### Login to Get Access Token

*POST /users/login/*

Request Body:

```json
{
  "login": "test_login",
  "password": "testpassword"
}
```

Response:

```json
{
  "token": "your_generated_jwt_token"
}
```

### Receipt Management

#### Create a Receipt

*POST /receipts/*

Request Body:

```json
{
  "payment": {
    "type": "cash",
    "amount": 200.0
  },
  "products": [
    {
      "name": "Apple",
      "price": 1.5,
      "quantity": 10
    },
    {
      "name": "Banana",
      "price": 1.2,
      "quantity": 5
    }
  ]
}
```

Response:

```json
{
  "id": 1,
  "products": [
    {
      "name": "Apple",
      "price": 1.5,
      "quantity": 10,
      "total": 15.0
    },
    {
      "name": "Banana",
      "price": 1.2,
      "quantity": 5,
      "total": 6.0
    }
  ],
  "payment": {
    "type": "cash",
    "amount": 200.0
  },
  "total": 21.0,
  "rest": 179.0,
  "created_at": "2025-02-21T12:00:00"
}
```

#### Get a List of Receipts

*GET /receipts/*

**Query Parameters:**
- `limit`: (default 100) Number of records to return.
- `offset`: (default 0) The starting point for records to return.

Response:

```json
[
  {
    "id": 1,
    "products": [
      {
        "name": "Apple",
        "price": 1.5,
        "quantity": 10,
        "total": 15.0
      },
      {
        "name": "Banana",
        "price": 1.2,
        "quantity": 5,
        "total": 6.0
      }
    ],
    "payment": {
      "type": "cash",
      "amount": 200.0
    },
    "total": 21.0,
    "rest": 179.0,
    "created_at": "2025-02-21T12:00:00"
  }
]
```

#### Get a Receipt by ID

*GET /receipts/{receipt_id}*

Response:

```json
{
  "id": 1,
  "products": [
    {
      "name": "Apple",
      "price": 1.5,
      "quantity": 10,
      "total": 15.0
    },
    {
      "name": "Banana",
      "price": 1.2,
      "quantity": 5,
      "total": 6.0
    }
  ],
  "payment": {
    "type": "cash",
    "amount": 200.0
  },
  "total": 21.0,
  "rest": 179.0,
  "created_at": "2025-02-21T12:00:00"
}
```

#### Get Receipt in Text Format

*GET /receipts/receipt-txt/{receipt_id}*

Response (Plain Text):

```
             test_user             
================================
10 x 1.5                   15.00
Apple
--------------------------------
5 x 1.2                     6.00
Banana
--------------------------------
================================
СУМА                       21.00
Готівка                   200.00
Решта                     179.00
================================
        21.02.2025 14:24        
      Дякуємо за покупку!  
```

## Running the Project

1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Set up the database and run migrations.
4. Run the FastAPI application using `uvicorn app.main:app --reload`.
5. Access the API at http://127.0.0.1:8000 or use http://127.0.0.1:8000/docs for documentation in OpenApi format.

## Environment Variables

- `SECRET_KEY`: The secret key for signing JWT tokens.
- `ALGORITHM`: The algorithm used to sign JWT tokens (default is HS256).
- `DATABASE_URL`: The connection string to your PostgreSQL database (e.g., `postgresql://user:password@localhost/dbname`).
