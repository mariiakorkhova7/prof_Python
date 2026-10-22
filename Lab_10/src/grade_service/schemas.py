from pydantic import BaseModel, Field

class StudentCreate(BaseModel):
    name: str
    group_name: str

class StudentOut(StudentCreate):
    id: int
    class Config:
        from_attributes = True

class GradeCreate(BaseModel):
    student_id: int
    subject: str
    value: float = Field(..., ge=0.0, le=100.0)

class GradeOut(GradeCreate):
    id: int
    class Config:
        from_attributes = True