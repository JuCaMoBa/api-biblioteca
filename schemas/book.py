from sqlalchemy import Column, Integer , String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__= "books"
    id     = Column(Integer, primary_key=True)
    title  = Column(String)
    author = Column(String)
    year   = Column(Integer)
    ISBN   = Column(String)
    
    




