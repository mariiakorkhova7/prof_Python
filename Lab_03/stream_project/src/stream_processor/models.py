from typing import NamedTuple
from collections.abc import Iterator


class GradeRecord(NamedTuple):
    student_id: int
    name: str
    discipline: str
    grade: float


class GradeRangeIterator(Iterator[int]):
    """Власний клас ітератора для генерації балів у заданому діапазоні з кроком."""

    def __init__(self, start: int, stop: int, step: int = 1) -> None:
        self.current = start
        self.stop = stop
        self.step = step

    def __iter__(self) -> "GradeRangeIterator":
        return self

    def __next__(self) -> int:
        if self.current >= self.stop:
            raise StopIteration
        value = self.current
        self.current += self.step
        return value


class GradeRange:
    """Власний клас Iterable, який повертає новий незалежний GradeRangeIterator."""

    def __init__(self, start: int, stop: int, step: int = 1) -> None:
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self) -> GradeRangeIterator:
        return GradeRangeIterator(self.start, self.stop, self.step)