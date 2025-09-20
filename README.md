# Simplified Event Ticketing System

This is a modular, production-ready FastAPI project for a simplified event ticketing system. It demonstrates key software engineering patterns including service-oriented architecture, secure authentication, external API integration, and the circuit breaker pattern for resilience.

## Features

-   **User Management**: Register and authenticate users with JWT.
-   **Event Catalog**: Public and secured endpoints for managing event data.
-   **Payment Processing**: Simulates secure payment processing with a Paystack API integration mock.
-   **Ticket Generation**: Generates QR code-based tickets and simulates sending them via email.
-   **Circuit Breaker**: The payment service is wrapped in a circuit breaker to handle API failures gracefully.

## Setup and Run

1.  **Clone the repository**:
    ```bash
    git clone [https://github.com/your-username/your-repo.git](https://github.com/your-username/your-repo.git)
    cd your-repo
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application**:
    ```bash
    uvicorn app.main:app --reload
    ```
    The application will run on `http://127.0.0.1:8000`.

## API Documentation & Usage

The API is self-documented. You can access the interactive documentation at:

-   **Swagger UI**: `http://127.0.0.1:8000/docs`
-   **ReDoc**: `http://127.0.0.1:8000/redoc`

**Example Workflow:**

1.  **Register a User**:
    `POST /users/` with `{"email": "test@example.com", "username": "testuser", "password": "password123"}`

2.  **Login to Get a Token**:
    `POST /token` with `x-www-form-urlencoded` body: `username=testuser` and `password=password123`. Copy the `access_token`.

3.  **Create an Event**:
    `POST /events/` with a body like `{"title": "Concert", "date": "2025-12-25T19:00:00Z", "location": "City Hall", "ticket_price": 50.0}`. No authentication is needed for this simple demo.

4.  **Initiate Payment & Get Ticket**:
    `POST /payments/pay` with body `{"event_id": 1}`. Add `Authorization: Bearer <your_token>` to the header.

5.  **Verify Payment & Generate Ticket**:
    `POST /payments/verify/{reference}` where `{reference}` is from the previous step. The ticket will be created.

6.  **Get Your Ticket with QR Code**:
    `GET /tickets/{ticket_id}` with `Authorization: Bearer <your_token>`.