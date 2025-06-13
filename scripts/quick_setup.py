"""
Quick database setup and server test
"""

import asyncio

from sqlalchemy import create_engine, text

from app.core.database import Base
from app.models.device import Device


async def setup_and_test():
    print("🔧 Setting up SQLite database...")

    # Create SQLite database
    engine = create_engine("sqlite:///vulntrack_dev.db", echo=True)

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Test connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in result]
        print(f"✅ Created tables: {tables}")

    print("✅ Database setup complete!")
    print("🚀 You can now start the server!")


if __name__ == "__main__":
    asyncio.run(setup_and_test())
