"""Pytest fixtures: a per-test SQLite in-memory database with the schema applied.

The v1 schema does not use any Postgres-specific features (no PostGIS,
no JSONB, no array columns), so SQLite is a fine substrate for fast unit
tests. When the schema gains Postgres-specific features, this fixture
will switch to a real Postgres test database.
"""

from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.models import Base, category, farm, tier, verification  # noqa: F401  register


@pytest.fixture
def db() -> Generator[Session, None, None]:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    session = TestSession()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()
