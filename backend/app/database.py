"""
Database connection setup using SQLAlchemy.
Reads DATABASE_URL from environment variables (.env file).

Engine creation is intentionally deferred until first use (lazy
initialization) so that the app can start even if the database driver
is not yet available in the current image.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Check your .env file.")

# Base class for all models — does not require an engine at import time
Base = declarative_base()

# Private singletons — populated on first access, not at import time
_engine = None
_SessionLocal = None


def get_engine():
    """
    Return the SQLAlchemy engine, creating it on the first call.

    Deferring engine creation prevents a ModuleNotFoundError for the
    database driver (e.g. mysqlclient) from crashing the app at import
    time before the new image has been built and deployed.
    """
    global _engine
    if _engine is None:
        _engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,  # Reconnect if connection drops
        )
    return _engine


def _get_session_local():
    """Return the SessionLocal factory, creating it on the first call."""
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=get_engine()
        )
    return _SessionLocal


def get_db():
    """
    Dependency that provides a database session.
    Closes the session when the request is finished.
    """
    db = _get_session_local()()
    try:
        yield db
    finally:
        db.close()
