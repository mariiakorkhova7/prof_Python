import pytest
from grades.book import GradeBook

def test_empty_gradebook():
    book = GradeBook()
    assert book.average_grade() == 0.0
    assert book.min_max_grade() == (0.0, 0.0)
    assert book.success_rate() == 0.0

def test_gradebook_calculations(populated_book):
    assert populated_book.average_grade() == pytest.approx(80.0)
    assert populated_book.min_max_grade() == (50.0, 100.0)
    assert populated_book.success_rate(pass_threshold=60.0) == pytest.approx(66.666, rel=1e-3)

def test_sorting(populated_book):
    sorted_records = populated_book.sort_by_grade(reverse=True)
    assert sorted_records[0].grade.value == 100.0
    assert sorted_records[-1].grade.value == 50.0