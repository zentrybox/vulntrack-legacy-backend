"""
Simple SQLite Database Setup for Development
Use this when PostgreSQL is not available
"""

import os
from sqlalchemy import create_engine
from app.core.database import Base
from app.models.device import Device  # Import to register the model


def setup_sqlite_db():
    """Set up SQLite database for development"""
    print("🔧 Setting up SQLite database for development...")
    print("=" * 50)

    # SQLite database file
    db_file = "vulntrack_dev.db"
    database_url = f"sqlite:///./{db_file}"

    try:
        # Create engine
        engine = create_engine(database_url, echo=False)

        # Create all tables
        print("🏗️  Creating database tables...")
        Base.metadata.create_all(bind=engine)

        print("✅ SQLite database created successfully!")
        print(f"📍 Database file: {os.path.abspath(db_file)}")
        print("📊 Created tables: devices")
        print("=" * 50)
        print("🚀 Database is ready for use!")

        # Update .env to use SQLite
        print("📝 Updating .env to use SQLite...")
        with open(".env", "r") as f:
            content = f.read()

        # Replace database URL
        updated_content = content.replace(
            "DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/analyzer-db",
            f"DATABASE_URL=sqlite+aiosqlite:///./{db_file}",
        )

        with open(".env", "w") as f:
            f.write(updated_content)

        print("✅ Environment configured for SQLite!")
        print(
            "💡 You can now start the server with: poetry run uvicorn app.main:app --reload"
        )

    except Exception as e:
        print(f"❌ Error setting up SQLite database: {e}")
        return False

    return True


if __name__ == "__main__":
    setup_sqlite_db()
