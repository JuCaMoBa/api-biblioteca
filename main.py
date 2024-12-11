from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import List, Optional

from models.book import BookCreate, BookResponse, BookUpdate
from schemas.book import Book
from database.database import get_db

import logging

app = FastAPI()



@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book_data: BookCreate,db: Session = Depends(get_db)):
    try:
        book = Book(title=book_data.title, author=book_data.author, year=book_data.year, ISBN=book_data.ISBN )
        db.add(book)
        db.commit()
        db.refresh(book)
        return book
    
    except SQLAlchemyError as e:
         logging.error(f"Error al crear el libro: {e}")
         raise HTTPException(status_code=500, detail="Error al crear el libro")
         
@app.get("/books", response_model=List[BookResponse])
async def get_books(
    author: Optional[str] = Query(None, alias="author", description="Filtrar por autor"),
    year: Optional[int] = Query(None, alias="year", description="Filtrar por año"),
    db: Session = Depends(get_db),   
    ):
    try:
        query = db.query(Book)
        if author:
            query = query.filter(Book.author == author) 
        if year:
            query = query.filter(Book.year == year)       
        books = query.all()
        return books
    
    except SQLAlchemyError as e:
        logging.error(f"Error al obtener los libros {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al acceder a los datos en la base de datos"
        )
    
@app.get("/books/{book_id}", response_model=BookResponse)
async def get_book_by_id(book_id: int, db: Session = Depends(get_db),):
    try:
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
                raise HTTPException(status_code=404, detail="Libro no encontrado")
        return book
    except SQLAlchemyError as e:
        logging.error(f"Error al buscar el libro {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al buscar el libro en la base de datos"
        )

@app.put("/books/{book_id}", response_model=BookResponse)
async def update_book(book_id: int, book_data: BookUpdate, db: Session = Depends(get_db),):
    try:
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
                raise HTTPException(status_code=404, detail="Libro no encontrado")
        
        if book_data.title:
            book.title = book_data.title
        if book_data.author:
            book.author = book_data.author
        if book_data.year:
            book.year = book_data.year
        if book_data.ISBN:
            book.ISBN = book_data.ISBN

        db.commit()    

        return book
    except SQLAlchemyError as e:
        logging.error(f"Error al actualizar el libro {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al actualizar el libro en la base de datos"
        )

@app.delete("/books/{book_id}")
async def delete_book(book_id: int, db: Session = Depends(get_db),):
    try:
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
                raise HTTPException(status_code=404, detail="Libro no encontrado")
        
        db.delete(book)
        db.commit()
        return {"message": f"el libro con ID {book_id} ha sido eliminado"}
    
    except SQLAlchemyError as e:
        logging.error(f"Error al eliminar el libro {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al eliminar el libro en la base de datos"
        )

@app.get("/books-search/", response_model=List[BookResponse])
async def search_books(
    title: Optional[str] = Query(None, alias="title", description="Filtrar por titulo"),
    author: Optional[str] = Query(None, alias="author", description="Filtrar por autor"),
    db: Session = Depends(get_db),
    ):
    try:    
        query = db.query(Book)

        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))        
        if author:
            query = query.filter(Book.author.ilike(f"%{author}%"))

        query = query.order_by(Book.id.asc()) 
        
        books = query.all()

        if not books:
            raise HTTPException(status_code=404, detail="No se encontraron libros con los filtros proporcionados")
        
        return books
    except SQLAlchemyError as e:
        logging.error(f"Error al realizar la búsqueda de libros {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al realizar la búsqueda en la base de datos"
        )


