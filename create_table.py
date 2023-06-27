import sqlite3
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, create_engine

Base = declarative_base()

class Game(Base):
    engine = create_engine('sqlite:///game')


