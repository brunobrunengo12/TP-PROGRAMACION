import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from database import get_session
from main import app


@pytest.fixture
def session():
    # Crea la base de datos SQLite en memoria para cada test
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    engine.dispose()


@pytest.fixture
def client(session):
    # Sobrescribe get_session para que la API use la base en memoria
    app.dependency_overrides[get_session] = lambda: session
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def socio(client):
    respuesta = client.post("/socios", json={"nombre": "Ana", "email": "ana@gmail.com"})
    return respuesta.json()


@pytest.fixture
def libro(client):
    respuesta = client.post(
        "/libros", json={"titulo": "Ficciones", "isbn": "111", "stock": 5, "anio": 1944}
    )
    return respuesta.json()