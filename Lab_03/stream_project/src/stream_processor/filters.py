from collections.abc import Iterable, Iterator
from stream_processor.models import GradeRecord


def validate_grades(rows: Iterable[dict[str, str]]) -> Iterator[GradeRecord]:
    """Streaming validation оцінок та полів запису студента."""
    for row in rows:
        try:
            student_id = int(row["student_id"])
            name = row["name"].strip()
            discipline = row["discipline"].strip()
            grade = float(row["grade"])
        except (ValueError, TypeError, KeyError):
            continue

        if student_id <= 0 or not name or not discipline:
            continue
        if not (0.0 <= grade <= 100.0):
            continue

        yield GradeRecord(
            student_id=student_id,
            name=name,
            discipline=discipline,
            grade=grade,
        )


def filter_by_discipline(
    records: Iterable[GradeRecord],
    target_discipline: str | None = None,
) -> Iterator[GradeRecord]:
    """Generator для filtering: фільтрує записи за назвою дисципліни."""
    for record in records:
        if target_discipline is None or record.discipline.lower() == target_discipline.lower():
            yield record


def filter_by_min_grade(
    records: Iterable[GradeRecord],
    min_grade: float,
) -> Iterator[GradeRecord]:
    """Generator для filtering: залишає оцінки не нижче заданого порогу."""
    for record in records:
        if record.grade >= min_grade:
            yield record