import logging
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from grade_service.config import get_settings
from grade_service.database import SessionLocal, engine, Base
from grade_service.schemas import StudentCreate, StudentOut, GradeCreate, GradeOut
from grade_service.repositories import StudentRepository, GradeRepository
from grade_service.services import GradeService

settings = get_settings()

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "environment": settings.environment,
    }

@app.post("/students", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    return StudentRepository.create(db, student)

@app.get("/students", response_model=list[StudentOut])
def list_students(db: Session = Depends(get_db)):
    return StudentRepository.get_all(db)

@app.post("/grades", response_model=GradeOut, status_code=status.HTTP_201_CREATED)
def create_grade(grade: GradeCreate, db: Session = Depends(get_db)):
    student = StudentRepository.get_by_id(db, grade.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return GradeRepository.create(db, grade)

@app.get("/students/{id}/average")
def get_student_average(id: int, db: Session = Depends(get_db)):
    student = StudentRepository.get_by_id(db, id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    avg = GradeService.calculate_student_average(db, id)
    return {"student_id": id, "average_grade": avg}

@app.get("/subjects")
def list_subjects():
    return {"subjects": ["Mathematics", "Physics", "Computer Science"]}