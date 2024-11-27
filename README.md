# Secure Payment API

A secure and scalable API built with **Flask** to manage user authentication, payment creation, and transaction tracking. This API is designed for developers to integrate seamless payment solutions with advanced security features and a developer-friendly interface.

## Features

- **User Authentication**
  - Secure user registration and login with JWT-based authentication.
  - Passwords are hashed using industry-standard encryption.

- **Payment Management**
  - Create, update, and track payments with status management.
  - Retrieve individual or all user-specific payment details.

- **Secure Architecture**
  - Token-based access with JWT for session management.
  - Protects sensitive data with robust error handling and validations.

- **Developer-Friendly Endpoints**
  - Clean and modular routes designed for easy integration.

## Tech Stack

- **Language**: Python 3.x
- **Framework**: Flask
- **Database**: SQLite (easily replaceable with PostgreSQL/MySQL for production)
- **Authentication**: JWT tokens, hashed passwords

## Getting Started

### Prerequisites

Make sure you have Python 3.x installed and set up in your environment.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/amritacharya022/secure-API-pay.git
   cd secure-API-pay
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

### Endpoints

- **User Management**
  - `POST /register`: Register a new user.
  - `POST /login`: Log in and retrieve a JWT token.

- **Payment Management**
  - `POST /payment`: Create a new payment.
  - `GET /payment/<payment_id>`: Retrieve details of a specific payment.
  - `GET /payments`: Retrieve all payments for the authenticated user.
  - `PUT /payment/<payment_id>`: Update the status of a payment.

- **Credits**
  - `GET /credits`: Displays credits and author details.

### Example Usage

1. Register a new user:
   ```bash
   curl -X POST -H "Content-Type: application/json" \
   -d '{"username": "testuser", "password": "password123"}' \
   http://127.0.0.1:5000/register
   ```

2. Log in to retrieve a token:
   ```bash
   curl -X POST -H "Content-Type: application/json" \
   -d '{"username": "testuser", "password": "password123"}' \
   http://127.0.0.1:5000/login
   ```

3. Use the token to create a payment:
   ```bash
   curl -X POST -H "Content-Type: application/json" -H "x-access-token: <your_token_here>" \
   -d '{"amount": 100.0, "currency": "USD"}' \
   http://127.0.0.1:5000/payment
   ```

## Contribution

Contributions are welcome! Feel free to fork this repository, make your changes, and submit a pull request.

## Credits

Developed with ❤️ by [Amrit Acharya](https://github.com/amritacharya022).

---

*Secure Payment API for developers who value security and simplicity.*
