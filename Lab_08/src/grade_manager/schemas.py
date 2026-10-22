from pydantic import BaseModel, Field

class StudentCreate(BaseModel):
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=2, max_length=100)

class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    model_config = {"from_attributes": True}

class SubjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)

class SubjectResponse(BaseModel):
    id: int
    name: str
    model_config = {"from_attributes": True}

class GradeCreate(BaseModel):
    student_id: int = Field(gt=0)
    subject_id: int = Field(gt=0)
    value: float = Field(ge=0, le=100)

class GradeUpdate(BaseModel):
    value: float = Field(ge=0, le=100)

class GradeResponse(BaseModel):
    id: int
    value: float
    student_id: int
    subject_id: int
    model_config = {"from_attributes": True}