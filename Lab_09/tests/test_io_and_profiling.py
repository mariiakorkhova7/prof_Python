import csv
from pathlib import Path
import pytest
from grade_system.analytics import cached_discipline_statistics
from grade_system.parallel import (
    get_processed_count,
    load_multiple_csv_parallel,
    reset_processed_counter,
)


def test_parallel_csv_import_and_lock(tmp_path: Path):
    file1 = tmp_path / "g1.csv"
    file2 = tmp_path / "g2.csv"

    for f in [file1, file2]:
        with open(f, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["student_name", "discipline", "grade"])
            writer.writerow(["Тестовий Т.", "Інформатика", "95.0"])

    reset_processed_counter()
    records = load_multiple_csv_parallel([file1, file2], workers=2)

    assert len(records) == 2
    assert get_processed_count() == 2


def test_caching_and_invalidation():
    cached_discipline_statistics.cache_clear()
    data = (80.0, 90.0, 100.0)

    # First call - cache miss
    res1 = cached_discipline_statistics("Математика", repo_version=1, values_tuple=data)
    info1 = cached_discipline_statistics.cache_info()
    assert info1.hits == 0

    # Second call with same version - cache hit
    res2 = cached_discipline_statistics("Математика", repo_version=1, values_tuple=data)
    info2 = cached_discipline_statistics.cache_info()
    assert info2.hits == 1

    # Call with incremented version - new key / invalidation
    _ = cached_discipline_statistics("Математика", repo_version=2, values_tuple=data)
    info3 = cached_discipline_statistics.cache_info()
    assert info3.misses == 2