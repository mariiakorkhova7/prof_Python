import pytest
from grade_system.analytics import (
    calculate_scores_sequential,
    generate_grades,
    statistics_numpy,
    statistics_python,
)
from grade_system.parallel import calculate_scores_processes, calculate_scores_threads


def test_numpy_vs_python_statistics_accuracy():
    grades = generate_grades(1_000)
    py_res = statistics_python(grades)
    np_res = statistics_numpy(grades)

    assert np_res["average"] == pytest.approx(py_res["average"], rel=1e-5)
    assert np_res["minimum"] == pytest.approx(py_res["minimum"], rel=1e-5)
    assert np_res["maximum"] == pytest.approx(py_res["maximum"], rel=1e-5)
    assert np_res["std"] == pytest.approx(py_res["std"], rel=1e-5)


def test_process_pool_correctness():
    small_grades = [60.0, 75.0, 90.0]
    seq_res = calculate_scores_sequential(small_grades)
    par_res = calculate_scores_processes(small_grades, workers=2, chunksize=1)

    assert par_res == seq_res