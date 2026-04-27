from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base

engine = create_engine("sqlite:///./students.db", echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
