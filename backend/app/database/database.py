"""
Database connection and session management using SQLAlchemy.

This module establishes the SQLite database engine, creates a configured
session factory, and provides a declarative base for all ORM models.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Generator

from app.core.config import settings

# Create the SQLAlchemy engine.
# `check_same_thread=False` is required for SQLite when used with FastAPI's
# async request handling, since requests may be served from different threads.
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,  # Set to True to log all SQL statements (useful for debugging)
)

# SessionLocal is a factory that produces new Session objects when called.
# autocommit=False and autoflush=False give us explicit control over transactions.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for all SQLAlchemy ORM models.
# Every model class should inherit from this.
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session per request.

    Yields a SQLAlchemy Session and ensures it is closed after the request
    completes, even if an exception occurs.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
