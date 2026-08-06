import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from app import database as db_module
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
    # Point the app's module-global engine at the in-memory engine so the
    # startup lifespan's create_tables() (and anything using SessionLocal)
    # operates on the in-memory database instead of the default file-based
    # ./habits.db. This keeps the tests isolated from the filesystem and avoids
    # touching any stale or committed habits.db file.
    original_engine = db_module.engine
    db_module.engine = engine
    try:
        with TestClient(app) as c:
            yield c
    finally:
        db_module.engine = original_engine
        app.dependency_overrides.clear()

@pytest.fixture
def habit(client):
    r = client.post("/habits", json={"name": "Read"})
    return r.json()
