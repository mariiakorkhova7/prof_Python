from collections import defaultdict
from collections.abc import Iterable, Iterator
from itertools import accumulate, chain, groupby, islice, pairwise
from typing import Any

from stream_processor.models import GradeRecord


def streaming_average_grade(records: Iterable[GradeRecord]) -> float:
    """Потокове обчислення середнього бала без збереження списку в пам'яті."""
    total = 0.0
    count = 0
    for record in records:
        total += record.grade
        count += 1
    return total / count if count > 0 else 0.0


def calculate_stream_statistics(records: Iterable[GradeRecord]) -> dict[str, Any]:
    """Однопрохідна потокова агрегація: count, average, min, max."""
    count = 0
    total = 0.0
    minimum: float | None = None
    maximum: float | None = None

    for record in records:
        grade = record.grade
        count += 1
        total += grade
        if minimum is None or grade < minimum:
            minimum = grade
        if maximum is None or grade > maximum:
            maximum = grade

    average = total / count if count > 0 else 0.0
    return {
        "count": count,
        "average": average,
        "minimum": minimum,
        "maximum": maximum,
    }


def sum_grades_with_genexp(records: Iterable[GradeRecord]) -> float:
    """Використання generator expression для підрахунку суми балів без створення list."""
    grades_gen = (record.grade for record in records)
    return float(sum(grades_gen))


def lazy_students_above_average(
    records: Iterable[GradeRecord],
    threshold: float,
) -> Iterator[tuple[int, str, float]]:
    """
    Lazy визначення студентів із середнім балом вище заданого порогу.
    Акумулює суму та кількість балів на студента, а потім ліниво віддає тих,
    у кого середній бал > threshold.
    """
    totals: dict[int, list[Any]] = defaultdict(lambda: ["", 0.0, 0])
    for rec in records:
        entry = totals[rec.student_id]
        entry[0] = rec.name
        entry[1] += rec.grade
        entry[2] += 1

    student_averages = (
        (student_id, str(data[0]), round(float(data[1]) / int(data[2]), 2))
        for student_id, data in totals.items()
        if int(data[2]) > 0
    )

    for student_id, name, avg_grade in student_averages:
        if avg_grade > threshold:
            yield (student_id, name, avg_grade)


def build_top_n_rating(
    records: Iterable[GradeRecord],
    n: int,
    threshold: float = 0.0,
) -> list[tuple[int, str, float]]:
    """Формування рейтингу студентів за середнім балом з обмеженням перших N результатів (islice)."""
    qualified_stream = lazy_students_above_average(records, threshold)
    sorted_students = sorted(qualified_stream, key=lambda item: item[2], reverse=True)
    return list(islice(sorted_students, n))


def group_by_discipline(records: Iterable[GradeRecord]) -> dict[str, dict[str, Any]]:
    """Групування записів за дисципліною за допомогою itertools.groupby після сортування."""
    sorted_records = sorted(records, key=lambda r: r.discipline)
    result: dict[str, dict[str, Any]] = {}

    for discipline, group_iter in groupby(sorted_records, key=lambda r: r.discipline):
        stats = calculate_stream_statistics(group_iter)
        result[discipline] = stats
    return result


def group_by_student(
    records: Iterable[GradeRecord], limit_students: int = 5
) -> dict[int, list[float]]:
    """Групування оцінок за student_id через itertools.groupby (повертає перших limit_students)."""
    sorted_records = sorted(records, key=lambda r: r.student_id)
    grouped: dict[int, list[float]] = {}

    for student_id, group_iter in islice(
        groupby(sorted_records, key=lambda r: r.student_id), limit_students
    ):
        grouped[student_id] = [r.grade for r in group_iter]
    return grouped


def demonstrate_itertools_features(records: Iterable[GradeRecord]) -> dict[str, Any]:
    """Демонстрація засобів itertools: islice, pairwise, accumulate, chain."""
    first_five_grades = list(islice((r.grade for r in records), 5))
    diffs = [round(curr - prev, 2) for prev, curr in pairwise(first_five_grades)]
    running_totals = [round(val, 2) for val in accumulate(first_five_grades)]
    chained_sample = list(chain(first_five_grades[:2], first_five_grades[2:4]))

    return {
        "sample_grades": first_five_grades,
        "pairwise_diffs": diffs,
        "accumulate_totals": running_totals,
        "chained_sample": chained_sample,
    }