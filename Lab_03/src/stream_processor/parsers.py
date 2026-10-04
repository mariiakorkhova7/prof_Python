import csv
from collections.abc import Iterable, Iterator
from typing import Any


def parse_csv_rows(lines: Iterable[str]) -> Iterator[dict[str, Any]]:
    """Generator для parsing: перетворює потік очищених рядків у словники."""
    reader = csv.DictReader(lines)
    yield from reader