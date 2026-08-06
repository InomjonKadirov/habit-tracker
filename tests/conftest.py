import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
import app.database as database
from app.database import Base, get_db
from app.main import app

@pytest.fixture
def client():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)

    def override_db():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_db] = override_db
    # Route the app's lifespan create_tables() at the in-memory engine too, so
    # the test suite never opens a file-based SQLite database (a stale/corrupt
    # habits.db on disk would otherwise make create_tables() fail).
    original_engine = database.engine
    database.engine = engine
    try:
        with TestClient(app) as c:
            yield c
    finally:
        database.engine = original_engine
        app.dependency_overrides.clear()

@pytest.fixture
def habit(client):
    r = client.post("/habits", json={"name": "Read"})
    return r.json()
