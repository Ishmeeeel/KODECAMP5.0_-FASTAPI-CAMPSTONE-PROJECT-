# app/routers/payments.py

import requests
import json
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from pybreaker import CircuitBreaker, CircuitBreakerError
from typing import Dict, Any
from app.database import get_session
from app.models import Ticket, User, Event
from app.auth import get_current_user_from_token
from sqlmodel import Session, select
from datetime import datetime, timezone

router = APIRouter(prefix="/payments", tags=["payments"])

# --- Circuit Breaker Setup ---
# A circuit breaker that trips after 3 consecutive failures and resets after 30 seconds.
paystack_breaker = CircuitBreaker(fail_max=3, reset_timeout=30)

# Simulate Paystack API calls
# In a real application, you would make actual HTTP requests to the Paystack API.
class MockPaystackAPI:
    def initiate_payment(self, email: str, amount: float):
        """Simulates initiating a payment with Paystack."""
        if email == "fail@test.com":
            raise requests.exceptions.RequestException("Simulated network failure")
        return {
            "status": True,
            "message": "Authorization URL created",
            "data": {
                "authorization_url": "https://paystack.com/pay/mock_url",
                "access_code": "mock_code",
                "reference": f"ref_{email}_{int(amount)}"
            }
        }

    def verify_payment(self, reference: str):
        """Simulates verifying a payment with Paystack."""
        if "fail" in reference:
            raise requests.exceptions.RequestException("Simulated network failure")
        return {
            "status": True,
            "message": "Verification successful",
            "data": {
                "reference": reference,
                "status": "success",
                "amount": 10000 # Amount in kobo
            }
        }

mock_paystack = MockPaystackAPI()

# --- Endpoints ---
class PaymentInitiation(BaseModel):
    event_id: int

@router.post("/pay", status_code=status.HTTP_200_OK)
def initiate_payment(
    payment: PaymentInitiation,
    token_data: Dict[str, Any] = Depends(get_current_user_from_token),
    session: Session = Depends(get_session)
):
    """
    Initiates a payment for an event ticket using Paystack.
    This endpoint is protected by the circuit breaker.
    """
    user = session.get(User, token_data["user_id"])
    event = session.get(Event, payment.event_id)

    if not user or not event:
        raise HTTPException(status_code=404, detail="User or event not found.")

    try:
        # The circuit breaker wraps the call to the external service
        response = paystack_breaker.call(mock_paystack.initiate_payment, user.email, event.ticket_price)
        return {"authorization_url": response["data"]["authorization_url"], "reference": response["data"]["reference"]}
    except CircuitBreakerError:
        # If the circuit is open, this error is raised immediately, handling the failure gracefully
        raise HTTPException(status_code=503, detail="Payment service is temporarily unavailable. Please try again later.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred with the payment service.")


@router.post("/verify/{reference}", status_code=status.HTTP_200_OK)
def verify_payment(
    reference: str,
    token_data: Dict[str, Any] = Depends(get_current_user_from_token),
    session: Session = Depends(get_session)
):
    """Verifies a payment and generates a ticket upon success."""
    try:
        verification_response = paystack_breaker.call(mock_paystack.verify_payment, reference)
    except CircuitBreakerError:
        raise HTTPException(status_code=503, detail="Payment service is temporarily unavailable. Please try again later.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred with the payment service.")
        
    if verification_response["data"]["status"] != "success":
        raise HTTPException(status_code=400, detail="Payment not successful.")

    # A simplified way to find the event based on the mock reference
    try:
        parts = reference.split('_')
        event_price = float(parts[-1])
        event = session.exec(select(Event).where(Event.ticket_price == event_price)).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found for this purchase.")
            
    except (ValueError, IndexError):
        raise HTTPException(status_code=400, detail="Invalid payment reference format.")

    # Create a new ticket for the user
    new_ticket = Ticket(
        user_id=token_data["user_id"],
        event_id=event.id
    )
    
    session.add(new_ticket)
    session.commit()
    session.refresh(new_ticket)

    return {"message": "Payment verified and ticket generated successfully!", "ticket_id": new_ticket.id}