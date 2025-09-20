# app/database.py

import os
from sqlmodel import create_engine, Session

# Define the database URL. We'll use SQLite for simplicity.
# The 'events.db' file will be created automatically in your project's root directory.
DATABASE_URL = "sqlite:///events.db"

# Create the database engine. `echo=True` will show all SQL commands in the terminal.
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

def get_session():
    """A FastAPI dependency to provide a database session."""
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    """Creates all database tables defined by SQLModel."""
    from app.models import SQLModel
    print("Creating database and tables...")
    SQLModel.metadata.create_all(engine)
    print("Database and tables created.")