from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class GradeRecord:
    student_name: str
    discipline: str
    grade: float

    def is_passing(self, threshold: float = 60.0) -> bool:
        return self.grade >= threshold


@dataclass
class AcademicReport:
    discipline: str
    average: float
    minimum: float
    maximum: float
    std_dev: float
    total_records: int