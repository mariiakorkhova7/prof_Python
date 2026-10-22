from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from pathlib import Path
from threading import Lock
from typing import List
from grade_system.analytics import heavy_grade_score
from grade_system.models import GradeRecord
from grade_system.repositories import load_grades_from_csv

# Синхронізація для спільного лічильника
_processed_lock = Lock()
_global_processed_count = 0


def reset_processed_counter() -> None:
    global _global_processed_count
    with _processed_lock:
        _global_processed_count = 0


def get_processed_count() -> int:
    with _processed_lock:
        return _global_processed_count


def increment_processed_count(delta: int = 1) -> None:
    global _global_processed_count
    with _processed_lock:
        _global_processed_count += delta


def calculate_scores_threads(grades: List[float], workers: int = 4) -> List[float]:
    """I/O або псевдо-паралельне виконання через ThreadPoolExecutor."""
    with ThreadPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(heavy_grade_score, grades))


def calculate_scores_processes(grades: List[float], workers: int = 4, chunksize: int = 1000) -> List[float]:
    """CPU-bound паралельне виконання через ProcessPoolExecutor."""
    with ProcessPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(heavy_grade_score, grades, chunksize=chunksize))


def load_multiple_csv_parallel(file_paths: List[Path], workers: int = 4) -> List[GradeRecord]:
    """I/O-bound експеримент: паралельне читання декількох CSV-файлів оцінок."""
    all_records = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = executor.map(load_grades_from_csv, file_paths)
        for record_list in results:
            all_records.extend(record_list)
            increment_processed_count(len(record_list))
    return all_records