from asyncio import sleep
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from schemas.book import Base, Book
from main import app
from database.database import get_db

# Configuración de la base de datos para pruebas
DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(bind=test_engine)

# Crear las tablas en la base de datos de prueba
Base.metadata.create_all(bind=test_engine)

# Sobrescribir la dependencia de get_session
def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Cliente de prueba
client = TestClient(app)

@pytest.fixture(scope="function")
def db():
    db = TestSessionLocal()
    yield db
    db.commit()
    db.close()

# Datos de prueba
book = {
    "title": "Test Book",
    "author": "Test Author",
    "year": 2023,
    "ISBN": "1234567890"
}

# Prueba para crear un libro
def test_create_book_endpoint(db):
    response = client.post("/books", json=book)
    assert response.status_code == 201
    assert response.json().get('id')   

def test_get_book_endpoint(db):
    #Se crea el libro en la BD y obtenemos el ID
    db.add(Book(**book))
    db.commit()
    book_in_db = db.query(Book).filter_by(title=book["title"]).first()

    #SE hace la petición
    response = client.get(f"/books/{book_in_db.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == book["title"]
    assert data["author"] == book["author"]
    assert data["year"] == book["year"]
    assert data["ISBN"] == book["ISBN"]


def test_update_book_endpoint(db):
    #Se crea el libro en la BD y obtenemos el ID
    db.add(Book(**book))
    db.commit()
    book_in_db = db.query(Book).filter_by(title=book["title"]).first()

    updated_book = {
        "title": "Test Book Update",
        "author": "Test Author Update",
        "year": 2030,
        "ISBN": "123456789X"
    }

    #Se hace la petición
    response = client.put(f"/books/{book_in_db.id}", json=updated_book)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == updated_book["title"]
    assert data["author"] == updated_book["author"]
    assert data["year"] == updated_book["year"]
    assert data["ISBN"] == updated_book["ISBN"] 


def test_delete_book_endpoint(db):
    # Crear un libro de prueba en la base de datos
    db.add(Book(**book))
    db.commit()
    book_in_db = db.query(Book).filter_by(title=book["title"]).first()

    #Se hace la petición
    response = client.delete(f"/books/{book_in_db.id}")

    # Verificar la respuesta
    assert response.status_code == 200

def test_search_books_by_title(db):
    # Crear libros de prueba
    books = [
        {"title": "Book One", "author": "Author A", "year": 2020, "ISBN": "123"},
        {"title": "Another Book", "author": "Author B", "year": 2021, "ISBN": "456"},
        {"title": "Special Book", "author": "Author C", "year": 2022, "ISBN": "789"},
    ]
    for book in books:
        db.add(Book(**book))
    db.commit()

    # Buscar por título
    response = client.get("/books-search", params={"title": "Book"})

    # Verificar la respuesta
    assert response.status_code == 200
    data = response.json()
    assert all("Book" in book["title"] for book in data)


def test_search_books_by_author(db):
    # Crear libros de prueba
    books = [
        {"title": "Book One", "author": "Author A", "year": 2020, "ISBN": "123"},
        {"title": "Another Book", "author": "Author B", "year": 2021, "ISBN": "456"},
        {"title": "Special Book", "author": "Author C", "year": 2022, "ISBN": "789"},
    ]
    for book in books:
        db.add(Book(**book))
    db.commit()

    # Buscar por autor
    response = client.get("/books-search", params={"author": "Author B"})

    # Verificar la respuesta
    assert response.status_code == 200
    data = response.json()
    assert data[0]["author"] == "Author B"


def test_search_books_no_results(db):
    # Crear libros de prueba
    books = [
        {"title": "Book One", "author": "Author A", "year": 2020, "ISBN": "123"},
        {"title": "Another Book", "author": "Author B", "year": 2021, "ISBN": "456"},
    ]
    for book in books:
        db.add(Book(**book))
    db.commit()

    # Buscar con filtros que no coinciden
    response = client.get("/books-search", params={"title": "Nonexistent", "author": "Unknown"})

    # Verificar la respuesta
    assert response.status_code == 404
    assert response.json()["detail"] == "No se encontraron libros con los filtros proporcionados"




