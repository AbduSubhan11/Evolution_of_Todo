from sqlmodel import create_engine, Session
from urllib.parse import urlparse
import os
from contextlib import contextmanager, asynccontextmanager
from typing import AsyncGenerator

# Get database URL from environment
database_url = os.getenv("NEON_DATABASE_URL", "sqlite:///./todo_app.db")

# For PostgreSQL, we might need to handle the connection differently
if database_url.startswith("postgresql://") or database_url.startswith("postgres://"):
    # Parse the URL to extract components
    parsed = urlparse(database_url)
    # For Neon, we'll use the connection string as is
    engine = create_engine(database_url)
else:
    # For SQLite (development)
    engine = create_engine(database_url, connect_args={"check_same_thread": False})

def get_session():
    with Session(engine) as session:
        yield session

@asynccontextmanager
async def get_session_context() -> AsyncGenerator[Session, None]:
    """
    Async context manager for database sessions
    """
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()