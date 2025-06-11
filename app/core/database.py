from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from app.core.config import settings

# Create sync engine for PostgreSQL
engine = create_engine(
    settings.sync_database_url,
    echo=settings.debug,
    pool_pre_ping=True
)

# Create session maker
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

# Create declarative base using SQLAlchemy 2.0 style
class Base(DeclarativeBase):
    pass

# Dependency to get DB session
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
