# app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Dict, Any
from app.database import get_session
from app.models import User, UserCreate, UserRead
from app.auth import get_password_hash, get_current_user_from_token

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(
    user: UserCreate,
    session: Session = Depends(get_session)
):
    """
    Registers a new user.
    - Hashes the password for security.
    - Checks if the user's email is already registered.
    """
    # Check if a user with the same email or username already exists
    existing_user = session.exec(
        select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create a new User instance with the hashed password
    db_user = User(
        email=user.email,
        username=user.username,
        password=get_password_hash(user.password)
    )

    # Add the new user to the database
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/me", response_model=UserRead)
def read_current_user(
    token_data: Dict[str, Any] = Depends(get_current_user_from_token),
    session: Session = Depends(get_session)
):
    """
    Retrieves the profile of the currently logged-in user.
    - Requires a valid JWT access token in the header.
    """
    user = session.get(User, token_data["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
