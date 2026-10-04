from collections.abc import Iterable, Iterator
from typing import NamedTuple


class GradeRecord(NamedTuple):
    student_id: int
    name: str
    discipline: str
    grade: float


class GradeRangeIterator(Iterator[int]):
    """Власний клас ітератора для генерації балів у заданому діапазоні з кроком."""

    def __init__(self, start: int, stop: int, step: int = 1) -> None:
        if step == 0:
            raise ValueError("GradeRangeIterator step argument must not be zero")
        self.current = start
        self.stop = stop
        self.step = step

    def __iter__(self) -> "GradeRangeIterator":
        return self

    def __next__(self) -> int:
        if (self.step > 0 and self.current >= self.stop) or (
            self.step < 0 and self.current <= self.stop
        ):
            raise StopIteration
        value = self.current
        self.current += self.step
        return value


class GradeRange(Iterable[int]):
    """Власний клас Iterable, який повертає новий незалежний GradeRangeIterator."""

    def __init__(self, start: int, stop: int, step: int = 1) -> None:
        if step == 0:
            raise ValueError("GradeRange step argument must not be zero")
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self) -> GradeRangeIterator:
        return GradeRangeIterator(self.start, self.stop, self.step)