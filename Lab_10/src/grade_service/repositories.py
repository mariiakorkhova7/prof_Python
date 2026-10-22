from sqlalchemy.orm import Session
from grade_service.models import StudentModel, GradeModel
from grade_service.schemas import StudentCreate, GradeCreate

class StudentRepository:
    @staticmethod
    def create(db: Session, student: StudentCreate) -> StudentModel:
        db_student = StudentModel(name=student.name, group_name=student.group_name)
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student

    @staticmethod
    def get_all(db: Session):
        return db.query(StudentModel).all()

    @staticmethod
    def get_by_id(db: Session, student_id: int):
        return db.query(StudentModel).filter(StudentModel.id == student_id).first()

class GradeRepository:
    @staticmethod
    def create(db: Session, grade: GradeCreate) -> GradeModel:
        db_grade = GradeModel(student_id=grade.student_id, subject=grade.subject, value=grade.value)
        db.add(db_grade)
        db.commit()
        db.refresh(db_grade)
        return db_grade

    @staticmethod
    def get_by_student(db: Session, student_id: int):
        return db.query(GradeModel).filter(GradeModel.student_id == student_id).all()