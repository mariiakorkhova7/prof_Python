from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from grade_service.database import Base

class StudentModel(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    group_name = Column(String, index=True)

    grades = relationship("GradeModel", back_populates="student", cascade="all, delete-orphan")

class GradeModel(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject = Column(String, index=True)
    value = Column(Float, nullable=False)

    student = relationship("StudentModel", back_populates="grades")