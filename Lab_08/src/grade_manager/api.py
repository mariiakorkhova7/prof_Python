from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import get_session, engine, Base
from .schemas import (
    StudentCreate, StudentResponse, 
    SubjectCreate, SubjectResponse, 
    GradeCreate, GradeUpdate, GradeResponse
)
from .services import GradeManagerService
from .external_api import fetch_many_averages

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Grade Manager API", version="1.0.0")

@app.post("/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(data: StudentCreate, session: Session = Depends(get_session)):
    service = GradeManagerService(session)
    return service.create_student(data)

@app.post("/subjects", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
async def create_subject(data: SubjectCreate, session: Session = Depends(get_session)):
    service = GradeManagerService(session)
    return service.create_subject(data)

@app.post("/grades", response_model=GradeResponse, status_code=status.HTTP_201_CREATED)
async def create_grade(data: GradeCreate, session: Session = Depends(get_session)):
    service = GradeManagerService(session)
    return service.create_grade(data)

@app.get("/students/{id}/grades", response_model=list[GradeResponse])
async def get_student_grades(id: int, session: Session = Depends(get_session)):
    service = GradeManagerService(session)
    return service.get_student_grades(id)

@app.get("/students/{id}/average", response_model=float)
async def get_student_average(id: int, session: Session = Depends(get_session)):
    service = GradeManagerService(session)
    return service.get_student_average(id)

@app.patch("/grades/{id}", response_model=GradeResponse)
async def update_grade(id: int, data: GradeUpdate, session: Session = Depends(get_session)):
    service = GradeManagerService(session)
    updated_grade = service.update_grade(id, data.value)
    if not updated_grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    return updated_grade

@app.delete("/grades/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_grade(id: int, session: Session = Depends(get_session)):
    service = GradeManagerService(session)
    success = service.delete_grade(id)
    if not success:
        raise HTTPException(status_code=404, detail="Grade not found")

@app.get("/students", response_model=list[StudentResponse])
async def search_students(min_average: float, session: Session = Depends(get_session)):
    service = GradeManagerService(session)
    return service.filter_students_by_average(min_average)

# Асинхронне завдання з HTTPX, Semaphore, Task, gather, timeout, retry[cite: 30, 44]
@app.post("/students/batch-average")
async def batch_student_averages(student_ids: list[int]):
    base_url = "http://127.0.0.1:8000"
    try:
        results = await fetch_many_averages(base_url, student_ids)
        return {"data": results}
    except Exception as e:
        raise HTTPException(status_code=504, detail=f"Batch operation failed: {str(e)}")