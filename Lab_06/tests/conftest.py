import pytest
from grades.models import Student, Discipline, Grade, AssessmentRecord
from grades.book import GradeBook

@pytest.fixture
def sample_record():
    return AssessmentRecord(Student(1, "Anna"), Discipline(101, "Math"), Grade(85.0))

@pytest.fixture
def populated_book():
    return GradeBook([
        AssessmentRecord(Student(1, "Anna"), Discipline(101, "Math"), Grade(90.0)),
        AssessmentRecord(Student(2, "Oleh"), Discipline(101, "Math"), Grade(50.0)),
        AssessmentRecord(Student(3, "Iryna"), Discipline(101, "Math"), Grade(100.0)),
    ])