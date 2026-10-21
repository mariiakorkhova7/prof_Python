import csv
import json
from pathlib import Path
from typing import Iterator, List
from .models import Student, Discipline, Grade, AssessmentRecord, GradeValidationError

class DataImportError(Exception):
    pass

def read_csv(file_path: Path) -> Iterator[AssessmentRecord]:
    with file_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                yield AssessmentRecord(
                    student=Student(int(row["student_id"]), row["student_name"]),
                    discipline=Discipline(int(row["discipline_id"]), row["discipline_name"]),
                    grade=Grade(float(row["grade"]))
                )
            except (KeyError, ValueError, GradeValidationError) as e:
                raise DataImportError(f"Malformed record: {row}") from e

def write_json(records: List[AssessmentRecord], file_path: Path) -> None:
    data = [
        {
            "student_id": r.student.student_id,
            "name": r.student.name,
            "discipline": r.discipline.name,
            "grade": r.grade.value
        }
        for r in records
    ]
    file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")