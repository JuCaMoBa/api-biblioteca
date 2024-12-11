from contextlib import contextmanager
import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

url = URL.create(
    drivername='postgresql',
    username=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    database= os.getenv('DB_DATABASE'),
    port=os.getenv('DB_PORT')
)


engine = create_engine(url)
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


