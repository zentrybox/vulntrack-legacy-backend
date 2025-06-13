import logging
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

logger = logging.getLogger(__name__)


def get_database_engine():
    """Get database engine with fallback to SQLite in development"""
    try:
        # Try PostgreSQL first
        engine = create_engine(
            settings.sync_database_url, echo=settings.debug, pool_pre_ping=True
        )
        # Test connection
        with engine.connect():
            pass
        logger.info("Using PostgreSQL database")
        return engine
    except OperationalError:
        if settings.environment == "development":
            logger.warning(
                "PostgreSQL not available, falling back to SQLite for development"
            )
            engine = create_engine(
                settings.development_database_url, echo=settings.debug
            )
            return engine
        else:
            logger.error("PostgreSQL connection failed in production environment")
            raise


# Create engine with automatic fallback
engine = get_database_engine()

# Create session maker
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# Create declarative base using SQLAlchemy 2.0 style
class Base(DeclarativeBase):
    pass


# Dependency to get DB session
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
