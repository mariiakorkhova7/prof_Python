from pathlib import Path
from grade_system.analytics import (
    cached_discipline_statistics,
    generate_grades,
    statistics_numpy,
    statistics_python,
)
from grade_system.profiling import run_cprofile_analysis, run_tracemalloc_analysis


def main() -> None:
    print("=== Lab 09: Variant 7 - Student Grade Evaluation System ===")
    data_size = 1_000_000
    print(f"Generating test dataset of {data_size} grades...")
    grades = generate_grades(data_size)

    py_stats = statistics_python(grades)
    np_stats = statistics_numpy(grades)

    print(f"Python Average: {py_stats['average']:.4f}, StdDev: {py_stats['std']:.4f}")
    print(f"NumPy Average:  {np_stats['average']:.4f}, StdDev: {np_stats['std']:.4f}")

    # Profiling execution
    results_dir = Path("results")
    run_cprofile_analysis(results_dir / "profile.prof", data_size=data_size)
    mem = run_tracemalloc_analysis(data_size=data_size)
    print(f"Peak Memory usage: {mem['peak_mb']:.2f} MB")


if __name__ == "__main__":
    main()