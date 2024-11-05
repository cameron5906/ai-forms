from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlmodel import SQLModel
from contextlib import asynccontextmanager

# Create in-memory SQLite database
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create a single engine instance
engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create all tables on startup
async def create_db_and_tables():
    """Create the database and all tables defined in SQLModel metadata."""
    async with engine.begin() as conn:
        print("Creating tables")
        await conn.run_sync(SQLModel.metadata.create_all)

# Dependency to get database session
@asynccontextmanager
async def get_db():
    """Provide a database session for use in a context."""
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
        await session.commit()
