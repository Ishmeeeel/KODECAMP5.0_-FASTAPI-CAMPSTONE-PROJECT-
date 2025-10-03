# Simplified Event Ticketing System

This is a modular, production-ready FastAPI project for a simplified event ticketing system. It demonstrates key software engineering patterns including **service-oriented architecture**, **secure authentication** (JWT), **external API integration** (Paystack mock), and the **circuit breaker pattern** for resilience.

## Features

-   **User Management**: Register and authenticate users using JWT.
-   **Event Catalog**: Public and secured endpoints for managing event data.
-   **Payment Processing**: Simulates secure payment processing with a Paystack API integration mock.
-   **Ticket Generation**: Generates QR code-based tickets and simulates sending them via email.
-   **Circuit Breaker**: The payment service is wrapped in a circuit breaker to handle API failures gracefully, ensuring service continuity.

---

## Setup and Run

1.  **Clone the repository**:
    ```bash
    git clone [https://github.com/Ishmeeeel/KODECAMP5.0_-FASTAPI-CAMPSTONE-PROJECT-](https://github.com/Ishmeeeel/KODECAMP5.0_-FASTAPI-CAMPSTONE-PROJECT-)
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application**:
    ```bash
    uvicorn app.main:app --reload
    ```
    The application will run locally on `http://127.0.0.1:8000`.

---

## API Documentation & Usage

The API is self-documented via FastAPI. You can access the interactive documentation at the following local endpoints:

-   **Swagger UI**: `http://127.0.0.1:8000/docs`
-   **ReDoc**: `http://127.0.0.1:8000/redoc`

**Example Workflow:**

1.  **Register a User**:
    `POST /users/` with `{"email": "test@example.com", "username": "testuser", "password": "password123"}`

2.  **Login to Get a Token**:
    `POST /token` (Form Data: `username=testuser`, `password=password123`). Copy the `access_token`.

3.  **Create an Event**:
    `POST /events/` with a sample body (Authentication not required for this endpoint in the demo).

4.  **Initiate Payment & Get Ticket**:
    `POST /payments/pay` with body `{"event_id": 1}`. Remember to add `Authorization: Bearer <your_token>` to the header.

5.  **Verify Payment & Generate Ticket**:
    `POST /payments/verify/{reference}` (where `{reference}` is from the previous step). The ticket is then generated.

6.  **Retrieve Ticket with QR Code**:
    `GET /tickets/{ticket_id}` with `Authorization: Bearer <your_token>`.

---

## 🔗 Live Application (Submission)

This application is deployed live and is accessible for review 24/7:

-   **Live Swagger UI Link:** [Event Ticketing System API on Render](https://kodecamp5-0-fastapi-campstone-project.onrender.com/docs)
   

## 📦 Submission Deliverables

The final required components for this project are included as follows:

1.  **Swagger UI Link:** Provided above.
2.  **Postman Collection:** The complete collection file (`Event_Ticketing_System_API.postman_collection.json`) is included in the root of this repository for easy import and testing.

---

## 💡 Note on Ticket Retrieval (QR Code Display)

The endpoint for retrieving a ticket (`GET /tickets/{ticket_id}`) is correctly configured to generate and return the QR code.

If you don't see the image when testing:

* This endpoint returns the **raw image file** (binary data), not a JSON object.
* The **Swagger UI** is primarily designed to display JSON/text and often cannot render binary image files.

To properly view the QR code image, please use a tool like **Postman** (which will display the image in its response panel) or access the live URL for the endpoint directly in a standard web browser.
