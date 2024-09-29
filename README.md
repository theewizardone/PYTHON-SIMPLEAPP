FastAPI Customer & Order Management System

A simple REST API to manage customers and orders using FastAPI, SQLAlchemy, and Pydantic. This project supports the creation of customers and orders, and includes SMS notifications for new orders.
Features

    Customer Management: Create and retrieve customer information.
    Order Management: Create and retrieve orders associated with customers.
    SMS Notifications: Sends an SMS notification to the customer when a new order is placed.
    Database: Uses SQLite for data persistence (can be switched to any SQL database).
    Dependency Injection: Uses FastAPI's Depends feature for database session management.

Tech Stack

    Backend Framework: FastAPI
    Database: SQLite (with SQLAlchemy ORM)
    SMS Service: Custom SMS service module (integrate with Twilio or any other SMS provider)
    Pydantic: Data validation and serialization
    Uvicorn: ASGI server

Installation
Prerequisites

    Python 3.10+
    Virtual environment tool (venv or virtualenv)
    SQLite (comes with Python)

Setup Instructions

    Clone the repository:

    bash

git clone https://github.com/your-username/fastapi-customer-order-system.git
cd fastapi-customer-order-system

Create and activate a virtual environment:

bash

python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate

Install dependencies:

bash

pip install -r requirements.txt

Run database migrations: This project uses SQLAlchemy for ORM and table creation. Ensure the models.py file is correct, and the database will automatically generate the necessary tables.

Run the application:

bash

    uvicorn main:app --reload

    This will start the server on http://127.0.0.1:8000.

API Endpoints
Customers

    Create Customer:
        POST /customers/
        Payload:

        json

{
  "name": "John Doe",
  "code": "+1234567890"
}

Response:

json

    {
      "id": 1,
      "name": "John Doe",
      "code": "+1234567890"
    }

Get Customers:

    GET /customers/
    Response:

    json

        [
          {
            "id": 1,
            "name": "John Doe",
            "code": "+1234567890"
          }
        ]

Orders

    Create Order:
        POST /orders/
        Payload:

        json

{
  "customer_id": 1,
  "item": "Laptop",
  "amount": 1200
}

Response:

json

    {
      "id": 1,
      "customer_id": 1,
      "item": "Laptop",
      "amount": 1200
    }

Get Orders:

    GET /orders/
    Response:

    json

        [
          {
            "id": 1,
            "customer_id": 1,
            "item": "Laptop",
            "amount": 1200
          }
        ]

SMS Notifications

When an order is placed, an SMS notification is sent to the customer using the phone number stored in the code field. Make sure the sms_service.py is properly configured with your SMS provider.
Project Structure

graphql

.
├── app
│   ├── main.py                # FastAPI application
│   ├── models.py              # SQLAlchemy models
│   ├── database.py            # Database connection and session management
│   ├── sms_service.py         # SMS sending logic (integrate with a provider like Twilio)
├── README.md
├── requirements.txt           # Project dependencies
└── ...

Testing

To add tests, you can use pytest. To install it, run:

bash

pip install pytest

Run tests with:

bash

pytest

Deployment

You can deploy this application on platforms such as Heroku, AWS, or any server that supports Python and FastAPI. Uvicorn can be used to serve the application in production.
Deployment on Heroku

    Create a Procfile:

    bash

web: uvicorn main:app --host 0.0.0.0 --port $PORT

Push to Heroku:

bash

    git add .
    git commit -m "Initial commit"
    heroku create
    git push heroku master

    Access the app using the Heroku URL provided.

Contributing

Feel free to fork the repository and submit pull requests. Contributions are welcome!
Steps to Host on GitHub:

    Create a GitHub repository:
        Go to GitHub and click on the "+" icon to create a new repository.
        Give it a name like fastapi-customer-order-system.

    Initialize the GitHub repository locally:

    bash

git init
git remote add origin https://github.com/your-username/fastapi-customer-order-system.git
git add .
git commit -m "Initial commit"
git push -u origin master




