from dataclasses import dataclass

class GradeValidationError(Exception):
    pass

@dataclass(frozen=True)
class Student:
    student_id: int
    name: str

@dataclass(frozen=True)
class Discipline:
    discipline_id: int
    name: str

@dataclass(frozen=True)
class Grade:
    value: float

    def __post_init__(self) -> None:
        if not (0.0 <= self.value <= 100.0):
            raise GradeValidationError("Grade must be between 0 and 100")

@dataclass(frozen=True)
class AssessmentRecord:
    student: Student
    discipline: Discipline
    grade: Grade