# analytics.py
from collections.abc import Callable
from .decorators import measure_time

def calculate_student_avg(student: dict) -> float:
    """Обчислює середній бал конкретного студента."""
    grades = student["grades"]
    return sum(grades) / len(grades) if grades else 0.0

def get_min_max_grades(student: dict) -> tuple[int, int]:
    """Повертає мінімальну та максимальну оцінки."""
    grades = student["grades"]
    return min(grades), max(grades)

def sort_by_avg_grade(students: list[dict], reverse: bool = True) -> list[dict]:
    """Сортує список студентів за їх середнім балом (lambda функція)."""
    return sorted(students, key=lambda s: calculate_student_avg(s), reverse=reverse)

def create_avg_grade_filter(minimum_avg: float) -> Callable[[dict], bool]:
    """Closure: створює функцію-фільтр за заданим мінімальним середнім балом."""
    def predicate(student: dict) -> bool:
        return calculate_student_avg(student) >= minimum_avg
    return predicate

def calculate_custom_avg(*grades: int) -> float:
    """Демонстрація використання *args для обчислення середнього."""
    return sum(grades) / len(grades) if grades else 0.0

def create_student_record(**fields) -> dict:
    """Демонстрація використання **kwargs для створення запису."""
    return dict(fields)

def determine_success(student: dict) -> str:
    """Визначення успішності студента за середнім балом."""
    avg = calculate_student_avg(student)
    if avg >= 90:
        return "Відмінно"
    elif avg >= 75:
        return "Добре"
    elif avg >= 60:
        return "Задовільно"
    return "Незадовільно"