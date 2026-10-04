import csv
from pathlib import Path
from collections.abc import Iterable, Iterator, Callable
from stream_processor.models import GradeRecord
from stream_processor.readers import read_lines, clean_lines
from stream_processor.parsers import parse_csv_rows
from stream_processor.filters import validate_grades, filter_by_discipline, filter_by_min_grade
from stream_processor.transformations import normalize_records


def build_pipeline(
    path: Path,
    discipline: str | None = None,
    min_grade: float = 0.0,
) -> Iterator[GradeRecord]:
    """Будує лінивий (lazy) потоковий конвеєр обробки оцінок студентів."""
    lines = read_lines(path)
    cleaned = clean_lines(lines)
    rows = parse_csv_rows(cleaned)
    valid = validate_grades(rows)
    by_disc = filter_by_discipline(valid, discipline)
    by_grade = filter_by_min_grade(by_disc, min_grade)
    transformed = normalize_records(by_grade)
    return transformed


def process_eager(
    path: Path,
    discipline: str | None = None,
    min_grade: float = 0.0,
) -> list[GradeRecord]:
    """Eager implementation: повністю завантажує та матеріалізує всі проміжні списки у RAM."""
    with path.open("r", encoding="utf-8", newline="") as file:
        all_lines = [line.strip() for line in file.readlines() if line.strip()]

    all_rows = list(csv.DictReader(all_lines))
    valid_records = list(validate_grades(all_rows))
    filtered_disc = [
        r for r in valid_records
        if discipline is None or r.discipline.lower() == discipline.lower()
    ]
    filtered_grade = [r for r in filtered_disc if r.grade >= min_grade]
    normalized = [
        r._replace(name=r.name.title(), discipline=r.discipline.strip(), grade=round(r.grade, 2))
        for r in filtered_grade
    ]
    return normalized


def find_first_lazy(
    records: Iterable[GradeRecord],
    predicate: Callable[[GradeRecord], bool],
) -> GradeRecord | None:
    """Пошук першого запису з миттєвим припиненням роботи (early termination)."""
    for record in records:
        if predicate(record):
            return record
    return None


def find_first_eager(
    path: Path,
    predicate: Callable[[GradeRecord], bool],
) -> GradeRecord | None:
    """Eager пошук: спочатку матеріалізує весь відфільтрований список у пам'ять."""
    all_records = process_eager(path)
    matched = [r for r in all_records if predicate(r)]
    return matched[0] if matched else None