from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

def get_engine(db_url: str):
    return create_engine(db_url, echo=False)

def get_session_factory(engine):
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)

def create_tables(engine):
    # Импортируем Base из models, чтобы SQLAlchemy увидел все таблицы
    from . import models 
    Base.metadata.create_all(bind=engine)
    