# app/routers/events.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Optional, Dict, Any
from app.database import get_session
from app.models import Event, EventCreate, EventRead
from app.auth import get_current_user_from_token

router = APIRouter(prefix="/events", tags=["events"])

@router.post("/", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(
    event: EventCreate,
    # This endpoint is public for now, as no admin role was specified.
    # In a real app, it would be secured.
    session: Session = Depends(get_session)
):
    """Creates a new event. (Requires Admin in a real-world scenario)."""
    db_event = Event.from_orm(event)
    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event

@router.get("/", response_model=List[EventRead])
def get_events(
    category: Optional[str] = Query(None, description="Filter by event category"),
    session: Session = Depends(get_session)
):
    """Public endpoint to list all events, with an optional filter by category."""
    query = select(Event)
    if category:
        query = query.where(Event.category == category)
    
    events = session.exec(query).all()
    return events

@router.get("/{event_id}", response_model=EventRead)
def get_event_by_id(
    event_id: int,
    session: Session = Depends(get_session)
):
    """Public endpoint to retrieve a single event by ID."""
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event