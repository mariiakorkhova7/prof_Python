import csv
from pathlib import Path
from statistics import mean
from time import perf_counter
from grade_system.analytics import (
    calculate_scores_sequential,
    generate_grades,
    statistics_numpy,
    statistics_python,
)
from grade_system.parallel import calculate_scores_processes, calculate_scores_threads


def measure_execution(func, *args, repeats: int = 3) -> float:
    times = []
    for _ in range(repeats):
        start = perf_counter()
        func(*args)
        elapsed = perf_counter() - start
        times.append(elapsed)
    return mean(times)


def run_benchmarks() -> None:
    results_path = Path("results/benchmark_results.csv")
    results_path.parent.mkdir(parents=True, exist_ok=True)

    datasets = [10_000, 100_000, 500_000]
    worker_counts = [1, 2, 4, 8]

    rows = []
    print("Running benchmarks...")

    for size in datasets:
        grades = generate_grades(size)

        # Baseline Python
        t_seq = measure_execution(calculate_scores_sequential, grades)
        rows.append({"Dataset": size, "Method": "Sequential", "Workers": 1, "Mean_Time_s": t_seq, "Speedup": 1.0})

        # NumPy stats vs Python stats
        t_py_stat = measure_execution(statistics_python, grades)
        t_np_stat = measure_execution(statistics_numpy, grades)
        speedup_np = t_py_stat / t_np_stat if t_np_stat > 0 else 0
        rows.append({"Dataset": size, "Method": "NumPy_Vectorized", "Workers": 1, "Mean_Time_s": t_np_stat, "Speedup": speedup_np})

        # ThreadPool & ProcessPool
        for w in worker_counts:
            t_th = measure_execution(calculate_scores_threads, grades, w)
            rows.append({"Dataset": size, "Method": "ThreadPool", "Workers": w, "Mean_Time_s": t_th, "Speedup": t_seq / t_th})

            t_pr = measure_execution(calculate_scores_processes, grades, w)
            rows.append({"Dataset": size, "Method": "ProcessPool", "Workers": w, "Mean_Time_s": t_pr, "Speedup": t_seq / t_pr})

    with open(results_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Dataset", "Method", "Workers", "Mean_Time_s", "Speedup"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Results successfully saved to {results_path}")


if __name__ == "__main__":
    run_benchmarks()