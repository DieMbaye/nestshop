import os

# Les tests n'utilisent JAMAIS la vraie base : une base SQLite en mémoire
os.environ["DATABASE_URL"] = "sqlite://"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.main as main_module
from app.database import Base, get_db
from app.main import app
from app.models import Product

engine_test = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SessionTest = sessionmaker(bind=engine_test, autoflush=False)


@pytest.fixture
def client(monkeypatch):
    """Une API de test avec une base neuve et 2 produits."""
    Base.metadata.create_all(engine_test)

    db = SessionTest()
    db.add_all(
        [
            Product(name="Panier test", description="Panier", price=15000, stock=10),
            Product(name="Sac test", description=None, price=12000, stock=1),
        ]
    )
    db.commit()
    db.close()

    def override_get_db():
        db = SessionTest()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr(main_module, "engine", engine_test)

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine_test)