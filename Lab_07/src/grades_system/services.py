from sqlalchemy.orm import Session
from sqlalchemy import select, func
from .models import Student, Grade

class GradeService:
    def __init__(self, session: Session):
        self.session = session

    def assign_batch_grades(self, student_id: int, subject_id: int, grades: list[float], semester: int = 1) -> None:
        """Транзакція: пакетне виставлення оцінок із rollback при некоректній оцінці."""
        try:
            for val in grades:
                if val < 0 or val > 100:
                    raise ValueError(f"Некоректна оцінка: {val}")
                grade = Grade(student_id=student_id, subject_id=subject_id, value=val, semester=semester)
                self.session.add(grade)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

    def get_students_above_threshold(self, threshold: float) -> list[tuple[str, float]]:
        """Пошук студентів із середнім балом вище порога."""
        statement = (
            select(Student.full_name, func.avg(Grade.value).label('avg_grade'))
            .join(Grade, Student.id == Grade.student_id)
            .group_by(Student.id)
            .having(func.avg(Grade.value) > threshold)
        )
        return list(self.session.execute(statement))