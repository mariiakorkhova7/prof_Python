from lab01.models import Student

def get_min_max_grades(student: Student) -> tuple[float, float]:
    if not student.grades:
        return 0.0, 0.0
    return min(student.grades), max(student.grades)

def is_successful(student: Student, passing_score: float = 60.0) -> bool:
    return student.average_grade >= passing_score

def sort_students(students: list[Student]) -> list[Student]:
    return sorted(students, key=lambda s: s.average_grade, reverse=True)

def filter_by_min_average(students: list[Student], min_average: float) -> list[Student]:
    return [s for s in students if s.average_grade > min_average]