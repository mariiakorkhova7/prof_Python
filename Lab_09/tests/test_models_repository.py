import pytest
from grade_system.models import GradeRecord
from grade_system.repositories import GradeRepository


def test_repository_add_and_filter():
    repo = GradeRepository()
    repo.add_record(GradeRecord("Іваненко І.І.", "Математика", 85.0))
    repo.add_record(GradeRecord("Петренко П.П.", "Математика", 55.0))

    all_records = repo.get_all()
    assert len(all_records) == 2

    passing = repo.filter_by_threshold(60.0)
    assert len(passing) == 1
    assert passing[0].student_name == "Іваненко І.І."


def test_repository_version_invalidation():
    repo = GradeRepository()
    v1 = repo.version
    repo.add_record(GradeRecord("Сидоренко С.С.", "Фізика", 90.0))
    assert repo.version == v1 + 1