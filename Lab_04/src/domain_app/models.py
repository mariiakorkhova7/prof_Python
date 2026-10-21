from dataclasses import dataclass, field
from typing import Iterator
from domain_app.value_objects import Score

@dataclass(frozen=True)
class Discipline:
    id: int
    name: str
    credits: float

@dataclass
class Grade:
    discipline: Discipline
    score: Score

    def __str__(self) -> str:
        return f"{self.discipline.name}: {self.score}"

class AssessmentRecord:
    def __init__(self) -> None:
        self._grades: list[Grade] = []

    def add_grade(self, grade: Grade) -> None:
        self._grades.append(grade)

    @property
    def average(self) -> float:
        if not self._grades:
            return 0.0
        return sum(g.score.value for g in self._grades) / len(self._grades)

    @property
    def min_score(self) -> float:
        if not self._grades:
            return 0.0
        return min(g.score.value for g in self._grades)

    @property
    def max_score(self) -> float:
        if not self._grades:
            return 0.0
        return max(g.score.value for g in self._grades)

    @property
    def is_successful(self) -> bool:
        if not self._grades:
            return False
        return self.min_score >= 51.0

    def __len__(self) -> int:
        return len(self._grades)

    def __iter__(self) -> Iterator[Grade]:
        return iter(self._grades)

@dataclass
class Person:
    id: int
    name: str

@dataclass
class Student(Person):
    group: str
    email: str
    record: AssessmentRecord = field(default_factory=AssessmentRecord)

    def __lt__(self, other: "Student") -> bool:
        return self.record.average < other.record.average

    def __str__(self) -> str:
        return f"[{self.id}] {self.name} ({self.group}) - Сер. бал: {self.record.average:.2f}"

@dataclass
class GradeBook:
    id: int
    name: str
    _students: list[Student] = field(default_factory=list)

    def add_student(self, student: Student) -> None:
        self._students.append(student)

    def __iter__(self) -> Iterator[Student]:
        return iter(self._students)

    def sort_by_average(self, descending: bool = True) -> list[Student]:
        return sorted(self._students, reverse=descending)

    def filter_above_threshold(self, threshold: float) -> list[Student]:
        return [s for s in self._students if s.record.average >= threshold]