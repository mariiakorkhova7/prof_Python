# main.py
import random
from .data import students_data
from .processors import (
    get_unique_disciplines, create_student_index, 
    group_by_discipline, count_disciplines
)
from .analytics import (
    calculate_student_avg, get_min_max_grades, sort_by_avg_grade, 
    create_avg_grade_filter, create_student_record, calculate_custom_avg,
    determine_success  # Додано імпорт функції визначення успішності
)
from .decorators import measure_time

def print_students(title: str, students: list[dict]):
    print(f"\n{title}")
    print("-" * 85)  # Збільшено ширину лінії для нового поля
    for s in students:
        avg = calculate_student_avg(s)
        status = determine_success(s)  # Виклик функції визначення успішності
        print(f"ID: {s['id']:<2} | ПІБ: {s['name']:<20} | Дисципліна: {s['discipline']:<15} | Сер. бал: {avg:.2f} | Статус: {status}")

@measure_time
def run_benchmark(records_count: int):
    """Бенчмарк для порівняння O(N) та O(1) пошуку."""
    print(f"\n--- Експериментальна частина: Benchmark ({records_count} записів) ---")
    
    # Генерація великих даних
    large_data = [
        {"id": i, "name": f"Student_{i}", "grades": (random.randint(60, 100),)}
        for i in range(1, records_count + 1)
    ]
    target_id = records_count - 5 # Шукаємо десь у кінці
    
    @measure_time
    def list_search(data, s_id):
        for s in data:
            if s["id"] == s_id:
                return s
        return None

    @measure_time
    def dict_search(data, s_id):
        index = {s["id"]: s for s in data} # Побудова O(N)
        return index.get(s_id) # Пошук O(1)

    print("Пошук у list (O(n)):")
    list_search(large_data, target_id)
    
    print("Побудова + Пошук у dict (пошук O(1)):")
    dict_search(large_data, target_id)


def main():
    print_students("Всі студенти", students_data)

    # Унікальні дисципліни (set)
    print(f"\nУнікальні дисципліни: {get_unique_disciplines(students_data)}")

    # Min/Max оцінки для першого студента
    min_g, max_g = get_min_max_grades(students_data[0])
    print(f"\nСтудент {students_data[0]['name']} - Min: {min_g}, Max: {max_g}")

    # Сортування
    sorted_students = sort_by_avg_grade(students_data)
    print_students("Студенти відсортовані за рейтингом", sorted_students)

    # Closure: Фільтрація (успішність вище 85)
    is_highly_successful = create_avg_grade_filter(85.0)
    # List comprehension
    successful_students = [s for s in students_data if is_highly_successful(s)]
    print_students("Студенти із середнім балом >= 85", successful_students)

    # Групування та Counter
    print("\nCounter дисциплін:")
    for disc, count in count_disciplines(students_data).items():
        print(f" - {disc}: {count} студент(ів)")

    grouped = group_by_discipline(students_data)
    print("\nГрупування за дисципліною 'Програмування':")
    for s in grouped.get("Програмування", []):
        print(f" -> {s['name']}")

    # dict-index
    index = create_student_index(students_data)
    print(f"\nШвидкий пошук за ID=3: {index.get(3)['name']}")

    # *args та **kwargs
    print(f"\nСередній бал через *args (90, 100, 85): {calculate_custom_avg(90, 100, 85):.2f}")
    new_s = create_student_record(id=99, name="Новий Студент", group="ФЕП-23")
    print(f"Створено через **kwargs: {new_s}")

    # Бенчмарк
    run_benchmark(100_000)

if __name__ == "__main__":
    main()