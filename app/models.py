# app/models.py

from typing import List, Optional, Union
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone

class UserBase(SQLModel):
    """Base model for User with common fields."""
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)

class User(UserBase, table=True):
    """Database table for a User."""
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str
    
    # Relationship to tickets (allows us to access a user's tickets)
    tickets: List["Ticket"] = Relationship(back_populates="user")

class UserCreate(UserBase):
    """Pydantic model for creating a new user."""
    password: str

class UserRead(UserBase):
    """Pydantic model for reading user data (hides the password)."""
    id: int

class EventBase(SQLModel):
    """Base model for an Event with common fields."""
    title: str = Field(index=True)
    date: datetime
    location: str
    ticket_price: float
    category: Optional[str] = None
    
class Event(EventBase, table=True):
    """Database table for an Event."""
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationship to tickets
    tickets: List["Ticket"] = Relationship(back_populates="event")

class EventCreate(EventBase):
    """Pydantic model for creating a new event."""
    pass
    
class EventRead(EventBase):
    """Pydantic model for reading event data."""
    id: int

class TicketBase(SQLModel):
    """Base model for a Ticket with common fields."""
    purchase_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_used: bool = False
    qr_code_base64: Optional[str] = None # Stores Base64 representation of the QR code

class Ticket(TicketBase, table=True):
    """Database table for a Ticket."""
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Foreign keys linking a ticket to a user and an event
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    event_id: Optional[int] = Field(default=None, foreign_key="event.id")
    
    # Relationships
    user: Optional[User] = Relationship(back_populates="tickets")
    event: Optional[Event] = Relationship(back_populates="tickets")

class TicketRead(TicketBase):
    """Pydantic model for reading ticket data."""
    id: int
    user_id: int
    event_id: int

# Paystack models for data validation
class PaystackPayment(SQLModel):
    """Model for initiating a Paystack payment."""
    email: str
    amount: float
    callback_url: str

class PaystackVerification(SQLModel):
    """Model for verifying a Paystack payment."""
    status: bool
    data: dict

class PaystackResponse(SQLModel):
    """Model for a generic Paystack API response."""
    status: bool
    message: str
    data: dict