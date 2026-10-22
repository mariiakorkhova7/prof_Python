from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from grade_service.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)
Base = declarative_base()