from typing import List
from .models import AssessmentRecord

class GradeBook:
    def __init__(self, records: List[AssessmentRecord] = None):
        self.records = records or []

    def add_record(self, record: AssessmentRecord) -> None:
        self.records.append(record)

    def average_grade(self) -> float:
        if not self.records:
            return 0.0
        return sum(r.grade.value for r in self.records) / len(self.records)

    def min_max_grade(self) -> tuple[float, float]:
        if not self.records:
            return (0.0, 0.0)
        grades = [r.grade.value for r in self.records]
        return min(grades), max(grades)

    def success_rate(self, pass_threshold: float = 60.0) -> float:
        if not self.records:
            return 0.0
        passed = sum(1 for r in self.records if r.grade.value >= pass_threshold)
        return (passed / len(self.records)) * 100

    def sort_by_grade(self, reverse: bool = True) -> List[AssessmentRecord]:
        return sorted(self.records, key=lambda r: r.grade.value, reverse=reverse)

    def get_students_above_threshold(self, threshold: float) -> List[AssessmentRecord]:
        return [r for r in self.records if r.grade.value >= threshold]