# app/routers/tickets.py

import base64
import qrcode
from io import BytesIO
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Dict, Any
from app.database import get_session
from app.models import Ticket, TicketRead
from app.auth import get_current_user_from_token

router = APIRouter(prefix="/tickets", tags=["tickets"])


def generate_qr_code(ticket_id: int, user_id: int):
    """
    Generates a QR code for a given ticket ID.
    The QR code data includes the ticket ID and user ID.
    """
    qr_data = f"Ticket ID: {ticket_id}, User ID: {user_id}"
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code image to an in-memory buffer
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return img_str


@router.get("/{ticket_id}", response_model=TicketRead)
def get_ticket(
    ticket_id: int,
    token_data: Dict[str, Any] = Depends(get_current_user_from_token),
    session: Session = Depends(get_session)
):
    """
    Retrieves a ticket for the current user and generates a QR code for it.
    The QR code is returned as a Base64 string.
    """
    # Find the ticket and ensure it belongs to the current user
    ticket = session.exec(
        select(Ticket).where(Ticket.id == ticket_id,
                             Ticket.user_id == token_data["user_id"])
    ).first()

    if not ticket:
        raise HTTPException(
            status_code=404, detail="Ticket not found or does not belong to you.")

    # Generate the QR code dynamically
    qr_code_base64 = generate_qr_code(ticket.id, ticket.user_id)
    ticket.qr_code_base64 = qr_code_base64

    # Simulate email sending
    print(f"Simulating email to user with QR code attached.")

    return ticket
