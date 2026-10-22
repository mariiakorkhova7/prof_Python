from sqlalchemy.orm import Session
from sqlalchemy import func
from .models import Student, Subject, Grade

class GradeRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_student(self, student: Student) -> Student:
        self.session.add(student)
        self.session.commit()
        self.session.refresh(student)
        return student

    def add_subject(self, subject: Subject) -> Subject:
        self.session.add(subject)
        self.session.commit()
        self.session.refresh(subject)
        return subject

    def add_grade(self, grade: Grade) -> Grade:
        self.session.add(grade)
        self.session.commit()
        self.session.refresh(grade)
        return grade

    def get_grades_by_student(self, student_id: int) -> list[Grade]:
        return self.session.query(Grade).filter(Grade.student_id == student_id).all()

    def get_student_average(self, student_id: int) -> float:
        avg = self.session.query(func.avg(Grade.value)).filter(Grade.student_id == student_id).scalar()
        return float(avg) if avg else 0.0

    def get_grade_by_id(self, grade_id: int) -> Grade | None:
        return self.session.query(Grade).filter(Grade.id == grade_id).first()

    def update_grade(self, grade: Grade, new_value: float) -> Grade:
        grade.value = new_value
        self.session.commit()
        self.session.refresh(grade)
        return grade

    def delete_grade(self, grade: Grade):
        self.session.delete(grade)
        self.session.commit()

    def get_students_by_min_average(self, min_avg: float) -> list[Student]:
        students = self.session.query(Student).all()
        result = []
        for s in students:
            if self.get_student_average(s.id) >= min_avg:
                result.append(s)
        return result