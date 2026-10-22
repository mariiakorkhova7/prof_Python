from sqlalchemy.orm import Session
from grade_service.repositories import StudentRepository, GradeRepository

class GradeService:
    @staticmethod
    def calculate_student_average(db: Session, student_id: int) -> float:
        grades = GradeRepository.get_by_student(db, student_id)
        if not grades:
            return 0.0
        return sum(g.value for g in grades) / len(grades)