"""
Database initialization script
Run this to create the database tables
"""
from app.core.database import engine, Base
from app.models.device import Device  # Import to register the model

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()
