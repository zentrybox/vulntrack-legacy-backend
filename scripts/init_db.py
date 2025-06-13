"""
Database initialization script
Run this to create the database tables

This script will:
1. Try to connect to PostgreSQL first
2. If PostgreSQL is not available, use SQLite for development
3. Create all necessary tables
"""

import os
import sys

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

from app.core.config import settings
from app.core.database import Base
from app.models.device import Device  # Import to register the model


def test_postgresql_connection():
    """Test if PostgreSQL is available"""
    try:
        postgres_url = settings.sync_database_url
        engine = create_engine(postgres_url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ PostgreSQL is available")
        return True, postgres_url
    except OperationalError as e:
        print(f"❌ PostgreSQL not available: {e}")
        return False, None


def create_tables():
    """Create all database tables"""
    print("🔧 Initializing VulnTrack Database...")
    print("=" * 50)

    # Check PostgreSQL availability
    postgres_available, postgres_url = test_postgresql_connection()

    if postgres_available:
        print("🐘 Using PostgreSQL database")
        database_url = postgres_url
    else:
        print("📁 PostgreSQL not available, using SQLite for development")
        database_url = settings.development_database_url
        print(f"📍 SQLite file: {os.path.abspath('vulntrack_dev.db')}")

    try:
        # Create engine
        engine = create_engine(database_url, echo=False)

        # Create all tables
        print("🏗️  Creating database tables...")
        Base.metadata.create_all(bind=engine)

        # Verify tables were created
        with engine.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                    if "sqlite" in database_url
                    else "SELECT tablename FROM pg_tables WHERE schemaname='public'"
                )
            )
            tables = [row[0] for row in result]

        print("✅ Database tables created successfully!")
        print(f"📊 Created tables: {', '.join(tables)}")
        print("=" * 50)
        print("🚀 Database is ready for use!")

        if not postgres_available:
            print("💡 To use PostgreSQL instead of SQLite:")
            print("   1. Install and start PostgreSQL")
            print("   2. Create database 'analyzer-db'")
            print("   3. Run this script again")

    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        sys.exit(1)


if __name__ == "__main__":
    create_tables()
