import logging
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

from grading_importer.exceptions import RecordValidationError
from grading_importer.models import GradeRecord
from grading_importer.readers import read_csv_rows
from grading_importer.validators import parse_record

logger = logging.getLogger(__name__)

@dataclass
class ImportStatistics:
    total: int = 0
    valid: int = 0
    invalid: int = 0

@contextmanager
def logged_operation(operation: str):
    logger.info("%s started", operation)
    start = perf_counter()
    try:
        yield
    except Exception:
        logger.exception("%s failed", operation)
        raise
    else:
        elapsed = perf_counter() - start
        logger.info("%s finished in %.6f s", operation, elapsed)

def import_grades(
    path: Path,
    *,
    allowed_disciplines: list[str],
    skip_invalid: bool,
    statistics: ImportStatistics,
) -> Iterator[GradeRecord]:
    for line_number, row in read_csv_rows(path):
        statistics.total += 1
        try:
            record = parse_record(
                row,
                allowed_disciplines=allowed_disciplines,
                line_number=line_number,
            )
        except RecordValidationError as error:
            statistics.invalid += 1
            logger.warning("Invalid record at line %s: %s", error.line_number, error)
            if skip_invalid:
                continue
            raise
        statistics.valid += 1
        yield record

def filter_by_passing_grade(
    records: Iterable[GradeRecord],
    passing_grade: float,
) -> Iterator[GradeRecord]:
    for record in records:
        if record.grade >= passing_grade:
            yield record