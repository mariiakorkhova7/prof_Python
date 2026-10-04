from collections.abc import Iterable, Iterator
from stream_processor.models import GradeRecord


def normalize_records(records: Iterable[GradeRecord]) -> Iterator[GradeRecord]:
    """Generator для transformation: нормалізує ПІБ студента, дисципліну та округлює бал."""
    for record in records:
        yield record._replace(
            name=record.name.title(),
            discipline=record.discipline.strip(),
            grade=round(record.grade, 2),
        )