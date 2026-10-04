from collections.abc import Iterable, Iterator
from itertools import islice
from stream_processor.models import GradeRecord


def batched_records(
    records: Iterable[GradeRecord],
    batch_size: int,
) -> Iterator[list[GradeRecord]]:
    """Batch processing: групує потік записів у пакети фіксованого розміру через islice."""
    if batch_size <= 0:
        raise ValueError("batch_size must be > 0")
    iterator = iter(records)
    while True:
        batch = list(islice(iterator, batch_size))
        if not batch:
            return
        yield batch