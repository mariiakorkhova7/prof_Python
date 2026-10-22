import csv
import json
from pathlib import Path
from typing import List, Optional
from grade_system.models import GradeRecord


class GradeRepository:
    def __init__(self) -> None:
        self._records: List[GradeRecord] = []
        self._version: int = 0

    @property
    def version(self) -> int:
        return self._version

    def add_record(self, record: GradeRecord) -> None:
        self._records.append(record)
        self._version += 1

    def add_bulk(self, records: List[GradeRecord]) -> None:
        self._records.extend(records)
        self._version += 1

    def get_all(self) -> List[GradeRecord]:
        return self._records.copy()

    def filter_by_threshold(self, min_grade: float) -> List[GradeRecord]:
        return [r for r in self._records if r.grade >= min_grade]

    def clear(self) -> None:
        self._records.clear()
        self._version += 1


def load_grades_from_csv(file_path: Path) -> List[GradeRecord]:
    """I/O-bound функція для зчитування файлу CSV."""
    records = []
    with open(file_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(
                GradeRecord(
                    student_name=row["student_name"],
                    discipline=row["discipline"],
                    grade=float(row["grade"]),
                )
            )
    return records


def save_grades_to_json(file_path: Path, records: List[GradeRecord]) -> None:
    data = [
        {"student_name": r.student_name, "discipline": r.discipline, "grade": r.grade}
        for r in records
    ]
    with open(file_path, mode="w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)