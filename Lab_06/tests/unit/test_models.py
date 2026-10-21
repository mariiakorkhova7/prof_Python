import pytest
from grades.models import Grade, GradeValidationError

@pytest.mark.parametrize("value", [0, 50.5, 100])
def test_valid_grade(value):
    grade = Grade(value)
    assert grade.value == pytest.approx(value)

@pytest.mark.parametrize("value", [-0.1, -50, 100.1, 200])
def test_invalid_grade(value):
    with pytest.raises(GradeValidationError, match="0 and 100"):
        Grade(value)