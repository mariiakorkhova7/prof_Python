import cProfile
import pstats
import tracemalloc
from pathlib import Path
from grade_system.analytics import generate_grades, statistics_python


def run_cprofile_analysis(output_file: Path, data_size: int = 1_000_000) -> None:
    """Профілювання часу та викликів за допомогою cProfile."""
    grades = generate_grades(data_size)
    profiler = cProfile.Profile()

    profiler.enable()
    statistics_python(grades)
    profiler.disable()

    output_file.parent.mkdir(parents=True, exist_ok=True)
    profiler.dump_stats(str(output_file))

    stats = pstats.Stats(profiler)
    stats.sort_stats("cumulative")
    print("=== TOP 10 CUMULATIVE TIME CALLS ===")
    stats.print_stats(10)


def run_tracemalloc_analysis(data_size: int = 1_000_000) -> dict:
    """Профілювання використання пам'яті через tracemalloc."""
    tracemalloc.start()

    grades = generate_grades(data_size)
    _ = statistics_python(grades)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "current_mb": current / (1024 * 1024),
        "peak_mb": peak / (1024 * 1024),
    }


if __name__ == "__main__":
    prof_path = Path("results/profile.prof")
    run_cprofile_analysis(prof_path)
    mem_info = run_tracemalloc_analysis()
    print(f"Memory Peak: {mem_info['peak_mb']:.2f} MB")