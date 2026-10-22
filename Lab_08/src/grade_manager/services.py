from sqlalchemy.orm import Session
from .models import Student, Subject, Grade
from .schemas import StudentCreate, SubjectCreate, GradeCreate
from .repositories import GradeRepository

class GradeManagerService:
    def __init__(self, session: Session):
        self.repository = GradeRepository(session)

    def create_student(self, data: StudentCreate) -> Student:
        """Створення нового студента з Pydantic-схеми"""
        student = Student(**data.model_dump())
        return self.repository.add_student(student)

    def create_subject(self, data: SubjectCreate) -> Subject:
        """Створення нової дисципліни"""
        subject = Subject(**data.model_dump())
        return self.repository.add_subject(subject)

    def create_grade(self, data: GradeCreate) -> Grade:
        """Додавання нової оцінки студенту"""
        # Тут можна додати додаткову бізнес-логіку (наприклад, перевірку чи існує студент)
        grade = Grade(**data.model_dump())
        return self.repository.add_grade(grade)

    def get_student_grades(self, student_id: int) -> list[Grade]:
        """Отримання всіх оцінок студента"""
        return self.repository.get_grades_by_student(student_id)

    def get_student_average(self, student_id: int) -> float:
        """Отримання середнього бала студента"""
        return self.repository.get_student_average(student_id)

    def update_grade(self, grade_id: int, new_value: float) -> Grade | None:
        """Оновлення оцінки. Повертає None, якщо оцінку не знайдено"""
        grade = self.repository.get_grade_by_id(grade_id)
        if not grade:
            return None
        return self.repository.update_grade(grade, new_value)

    def delete_grade(self, grade_id: int) -> bool:
        """Видалення оцінки. Повертає False, якщо оцінку не знайдено"""
        grade = self.repository.get_grade_by_id(grade_id)
        if not grade:
            return False
        self.repository.delete_grade(grade)
        return True

    def filter_students_by_average(self, min_average: float) -> list[Student]:
        """Фільтрація студентів за мінімальним середнім балом"""
        return self.repository.get_students_by_min_average(min_average)