import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from schemas.book import Base, Book
from main import app
from database.database import get_session

# Configuración de la base de datos para pruebas
DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Crear las tablas en la base de datos de prueba
Base.metadata.create_all(bind=test_engine)

# Sobrescribir la dependencia de get_session
@pytest.fixture(scope="module")
def test_db_session():
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

app.dependency_overrides[get_session] = test_db_session

# Cliente de prueba
client = TestClient(app)

# Datos de prueba
sample_book = {
    "title": "Test Book",
    "author": "Test Author",
    "year": 2023,
    "ISBN": "1234567890"
}

# Prueba para crear un libro
def test_create_book():
    response = client.post("/books", json=sample_book)
    assert response.status_code == 201

def test_sample_book_in_database(test_db_session):
    book = test_db_session.query(Book).filter_by(title=sample_book["title"]).first()
    assert book is not None
    assert book.title == sample_book["title"]
    assert book.author == sample_book["author"]
    assert book.year == sample_book["year"]
    assert book.ISBN == sample_book["ISBN"]



