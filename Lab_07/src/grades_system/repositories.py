from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import Student, Subject, Grade

class StudentRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, full_name: str) -> Student:
        student = Student(full_name=full_name)
        self.session.add(student)
        self.session.commit()
        self.session.refresh(student)
        return student

    def get_by_id(self, student_id: int) -> Student | None:
        return self.session.get(Student, student_id)

    def delete(self, student_id: int) -> bool:
        student = self.get_by_id(student_id)
        if student:
            self.session.delete(student)
            self.session.commit()
            return True
        return False

class SubjectRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, name: str) -> Subject:
        subject = Subject(name=name)
        self.session.add(subject)
        self.session.commit()
        self.session.refresh(subject)
        return subject

    def get_all(self) -> list[Subject]:
        return list(self.session.scalars(select(Subject)))

class GradeRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def update_grade(self, grade_id: int, new_value: float) -> Grade | None:
        grade = self.session.get(Grade, grade_id)
        if grade:
            grade.value = new_value
            self.session.commit()
            self.session.refresh(grade)
            return grade
        return None