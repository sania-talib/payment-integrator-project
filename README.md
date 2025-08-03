External Payment Gateway Integrator
Project Purpose
This project demonstrates an understanding of modern software engineering practices by building a tool that simulates the core functions of a Payment Gateway Integrator. It is designed to process and log payment transactions, providing a crucial operational tool for troubleshooting and monitoring API interactions with external services.

Key Features
This Flask application provides the following RESTful API endpoints:

POST /api/process-payment

Function: Simulates sending a payment request to an external gateway (using a mock API).

Demonstrates: API integration, handling HTTP requests, and robust error handling.

GET /api/payments/failed

Function: Queries the MySQL database to retrieve all transactions that failed or returned an error.

Demonstrates: Operational troubleshooting techniques and the ability to write basic-to-advanced SQL queries.

Operational & Troubleshooting Showcase
This project's core value for a Product Operations role lies in its ability to log every transaction. This logging mechanism allows us to:

Identify Failed Transactions: The /api/payments/failed endpoint acts as a first-line troubleshooting tool to quickly find and report issues.

Diagnose Root Causes: The database logs the full request and response payloads, as well as the error message, providing the necessary data to diagnose why an external API call failed (e.g., a 401 Unauthorized error).

Monitor Performance: By logging the full transaction, the system provides a foundation for future monitoring and analysis.

Technical Stack
Backend: Python 3.x

Web Framework: Flask

Database: MySQL

Libraries: mysql-connector-python, requests

Version Control: Git & GitHub

How to Run the Project
Clone the Repository:
git clone https://github.com/sania-talib/payment-integrator-project.git

Set up the Virtual Environment:
python -m venv venv
source venv/bin/activate (macOS/Linux) or venv\Scripts\activate.ps1 (Windows PowerShell)

Install Dependencies:
pip install -r requirements.txt (This assumes you have created the requirements.txt file)

Set up MySQL Database:

Log into your MySQL client.

Create a user and database: CREATE DATABASE payment_integrator;

Update your db_config in db_ops.py with your MySQL credentials.

Run the database initialization script: python init_db.py

Run the Flask Application:
flask run

Use the Web Interface:
Open your browser and navigate to http://127.0.0.1:5000/ to use the web-based form to submit payment requests.