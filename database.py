"""
This module handles the database setup and session management
for the customer and orders system.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Database connection URL for SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./custom_orders.db"

# Create a new SQLAlchemy engine instance
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

def get_db():
    """
    This function creates a new database session and closes it once it's no longer needed.
    It acts as a dependency for FastAPI to ensure each request has its own session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Ensure the session is closed after use

