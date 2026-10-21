# processors.py
from collections import Counter, defaultdict

def get_unique_disciplines(students: list[dict]) -> set[str]:
    """Повертає множину унікальних дисциплін (Set comprehension)."""
    return {student["discipline"] for student in students}

def create_student_index(students: list[dict]) -> dict[int, dict]:
    """Створює словник для швидкого пошуку за ID (Dict comprehension)."""
    return {student["id"]: student for student in students}

def group_by_discipline(students: list[dict]) -> dict[str, list[dict]]:
    """Групує студентів за дисциплінами за допомогою defaultdict."""
    result = defaultdict(list)
    for student in students:
        result[student["discipline"]].append(student)
    return dict(result)

def count_disciplines(students: list[dict]) -> Counter:
    """Підраховує кількість записів для кожної дисципліни за допомогою Counter."""
    return Counter(student["discipline"] for student in students)