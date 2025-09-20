# app/main.py

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from app.database import create_db_and_tables, get_session
from app.models import User
from app.auth import verify_password, create_access_token
from app.routers import users, events, payments, tickets

app = FastAPI(
    title="Event Ticketing System API",
    description="A modular FastAPI project for managing events, users, and ticket purchases.",
    version="1.0.0"
)

# CORS configuration
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
app.include_router(users.router)
app.include_router(events.router)
app.include_router(payments.router)
app.include_router(tickets.router)


# The other routers will be included as we build them
# app.include_router(events.router)
# app.include_router(payments.router)
# app.include_router(tickets.router)

# --- Authentication Endpoint ---


@app.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    """
    Endpoint to get a JWT access token for authentication.
    Requires a username and password.
    """
    user = session.exec(select(User).where(
        User.username == form_data.username)).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- Startup Event ---


@app.on_event("startup")
def on_startup():
    """Initializes the database and tables when the application starts."""
    create_db_and_tables()
