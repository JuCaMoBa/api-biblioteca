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
Session = sessionmaker(bind=engine)

# Context Manager para manejar la sesión
@contextmanager
def get_session():
    session = Session()
    try:
        yield session  
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise e
    finally:
        session.close()
