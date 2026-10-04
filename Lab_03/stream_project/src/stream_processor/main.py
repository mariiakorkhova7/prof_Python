import time
import tracemalloc
from collections.abc import Callable
from contextlib import closing
from itertools import islice
from pathlib import Path
from typing import Any

from stream_processor.analytics import (
    build_top_n_rating,
    calculate_stream_statistics,
    demonstrate_itertools_features,
    group_by_discipline,
    group_by_student,
    lazy_students_above_average,
    streaming_average_grade,
    sum_grades_with_genexp,
)
from stream_processor.batches import batched_records
from stream_processor.models import GradeRange, GradeRecord
from stream_processor.pipeline import (
    build_pipeline,
    find_first_eager,
    find_first_lazy,
    process_eager,
)
from stream_processor.readers import generate_test_dataset


def measure_execution(func: Callable[..., Any], *args: Any) -> tuple[Any, float, float]:
    """Вимірює elapsed time (с) та peak memory (КБ) за допомогою tracemalloc."""
    tracemalloc.start()
    tracemalloc.reset_peak()
    start_time = time.perf_counter()
    result = func(*args)
    elapsed = time.perf_counter() - start_time
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, elapsed, peak_bytes / 1024.0


def benchmark_eager(path: Path) -> dict[str, Any]:
    records = process_eager(path, discipline="Programming", min_grade=60.0)
    return calculate_stream_statistics(records)


def benchmark_lazy(path: Path) -> dict[str, Any]:
    pipeline = build_pipeline(path, discipline="Programming", min_grade=60.0)
    return calculate_stream_statistics(pipeline)


def measure_time_to_first_result(path: Path) -> tuple[float, float]:
    """Порівнює час отримання першого елемента в Eager та Lazy режимах."""
    t0 = time.perf_counter()
    eager_list = process_eager(path, discipline="Programming", min_grade=90.0)
    _ = eager_list[0] if eager_list else None
    eager_ttfr = time.perf_counter() - t0

    t1 = time.perf_counter()
    with closing(build_pipeline(path, discipline="Programming", min_grade=90.0)) as lazy_pipe:
        _ = next(lazy_pipe, None)
    lazy_ttfr = time.perf_counter() - t1

    return eager_ttfr, lazy_ttfr


def main() -> None:
    data_dir = Path("data")
    main_csv = data_dir / "input.csv"

    print("=== 1. Демонстрація власного Iterable та Iterator ===")
    grade_scale = GradeRange(60, 101, 10)
    print("Перший прохід GradeRange:", list(grade_scale))
    print("Повторний прохід GradeRange (незалежний ітератор):", list(grade_scale))

    print("\n=== 2. Генерація основного датасету (100 000 записів) ===")
    generate_test_dataset(main_csv, count=100_000)
    print(f"Файл створено: {main_csv} (100 000 records)")

    print("\n=== 3. Потокова обробка (Варіант 7: Programming, grade >= 60) ===")
    with closing(build_pipeline(main_csv, discipline="Programming", min_grade=60.0)) as pipeline:
        first_5 = list(islice(pipeline, 5))
    print("Перші 5 записів з потоку (через islice):")
    for rec in first_5:
        print(f"  ID: {rec.student_id} | {rec.name} | {rec.discipline} | {rec.grade}")

    # Повторне створення pipeline для повної статистики
    pipeline = build_pipeline(main_csv, discipline="Programming", min_grade=60.0)
    stats = calculate_stream_statistics(pipeline)
    print(
        f"\nСтатистика (Programming): Count={stats['count']}, "
        f"Avg={stats['average']:.2f}, Min={stats['minimum']}, Max={stats['maximum']}"
    )

    # Перевірка streaming_average_grade та generator expression
    avg_only = streaming_average_grade(build_pipeline(main_csv, discipline="Algorithms"))
    total_sum = sum_grades_with_genexp(build_pipeline(main_csv, discipline="Algorithms"))
    print(f"Algorithms Streaming Average: {avg_only:.2f}, Sum (via genexp): {total_sum:.2f}")

    print("\n=== 4. Lazy визначення студентів із середнім балом > 85.0 та Топ-5 рейтинг ===")
    above_85_stream = lazy_students_above_average(build_pipeline(main_csv), threshold=85.0)
    print("Перші 3 студенти з середнім балом > 85.0 (lazy):")
    for st in islice(above_85_stream, 3):
        print(f"  Student ID: {st[0]}, Name: {st[1]}, Avg Grade: {st[2]}")

    top_5 = build_top_n_rating(build_pipeline(main_csv), n=5, threshold=80.0)
    print("Топ-5 рейтинг студентів:")
    for rank, st in enumerate(top_5, start=1):
        print(f"  #{rank}: ID={st[0]} ({st[1]}) — Avg: {st[2]}")

    print("\n=== 5. Групування за дисципліною та студентом (itertools.groupby) ===")
    disc_groups = group_by_discipline(build_pipeline(main_csv))
    for disc, d_stats in disc_groups.items():
        print(f"  {disc:15s} -> count: {d_stats['count']}, avg: {d_stats['average']:.2f}")

    student_groups = group_by_student(build_pipeline(main_csv), limit_students=3)
    print("Оцінки перших 3 студентів за ID:", student_groups)

    print("\n=== 6. Демонстрація Batch Processing (batch_size=25000) ===")
    batch_counts = [
        len(batch)
        for batch in batched_records(build_pipeline(main_csv), batch_size=25_000)
    ]
    print("Розміри отриманих батчів:", batch_counts)

    print("\n=== 7. Додаткові засоби itertools (pairwise, accumulate, chain) ===")
    with closing(build_pipeline(main_csv)) as pipe_for_demo:
        it_demo = demonstrate_itertools_features(pipe_for_demo)
    print("  Вибірка оцінок:", it_demo["sample_grades"])
    print("  Pairwise різниці:", it_demo["pairwise_diffs"])
    print("  Accumulate суми:", it_demo["accumulate_totals"])

    print("\n=== 8. Експеримент: Порівняння Eager vs Lazy (10k, 100k, 500k) ===")
    sizes = [10_000, 100_000, 500_000]
    print(
        f"{'Records':>10} | {'Eager Time (s)':>14} | {'Lazy Time (s)':>13} | "
        f"{'Eager Mem (KB)':>14} | {'Lazy Mem (KB)':>13} | {'Eager TTFR (s)':>14} | {'Lazy TTFR (s)':>13}"
    )
    print("-" * 105)

    for size in sizes:
        test_path = data_dir / f"dataset_{size}.csv"
        generate_test_dataset(test_path, count=size)

        _, e_time, e_mem = measure_execution(benchmark_eager, test_path)
        _, l_time, l_mem = measure_execution(benchmark_lazy, test_path)
        e_ttfr, l_ttfr = measure_time_to_first_result(test_path)

        print(
            f"{size:10d} | {e_time:14.4f} | {l_time:13.4f} | "
            f"{e_mem:14.2f} | {l_mem:13.2f} | {e_ttfr:14.6f} | {l_ttfr:13.6f}"
        )

    print("\n=== 9. Дослідження Early Termination (на прикладі 500 000 записів) ===")
    large_path = data_dir / "dataset_500000.csv"

    def predicate(r: GradeRecord) -> bool:
        return r.discipline == "Philosophy" and r.grade >= 98.0

    def run_lazy_find(p: Path, pred: Callable[[GradeRecord], bool]) -> GradeRecord | None:
        with closing(build_pipeline(p)) as stream:
            return find_first_lazy(stream, pred)

    _, eager_et_time, eager_et_mem = measure_execution(find_first_eager, large_path, predicate)
    _, lazy_et_time, lazy_et_mem = measure_execution(run_lazy_find, large_path, predicate)
    print(f"Eager find_first: time={eager_et_time:.5f} s, peak_mem={eager_et_mem:.2f} KB")
    print(f"Lazy  find_first: time={lazy_et_time:.5f} s, peak_mem={lazy_et_mem:.2f} KB")


if __name__ == "__main__":
    main()