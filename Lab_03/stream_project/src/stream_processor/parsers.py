import csv
from collections.abc import Iterable, Iterator


def parse_csv_rows(lines: Iterable[str]) -> Iterator[dict[str, str]]:
    """Generator для parsing: перетворює потік очищених рядків у словники."""
    reader = csv.DictReader(lines)
    yield from reader