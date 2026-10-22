from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from collections.abc import Generator

SQLALCHEMY_DATABASE_URL = "sqlite:///./grades.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_session() -> Generator:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()