from lab01.models import Student
from lab01.services import (
    get_min_max_grades, 
    is_successful, 
    sort_students, 
    filter_by_min_average
)

def main() -> None:
    students = [
        Student("Олег Мельник", "Бази даних", [75.0, 80.0, 60.0]),
        Student("Анна Коваль", "Комп'ютерні мережі", [50.0, 45.0, 55.0]),
        Student("Марія", "Професійний Python", [95.0, 98.0, 100.0])
    ]
    
    print("Рейтинг студентів:")
    for s in sort_students(students):
        min_g, max_g = get_min_max_grades(s)
        status = "Зараховано" if is_successful(s) else "Не зараховано"
        print(f"{s.full_name} | Сер: {s.average_grade:.1f} | Мін: {min_g}, Макс: {max_g} | {status}")

    min_threshold = 85.0
    print(f"\nСтуденти з балом вище {min_threshold}:")
    for s in filter_by_min_average(students, min_threshold):
        print(f"- {s.full_name} ({s.subject})")

if __name__ == "__main__":
    main()