from domain_app.dto import StudentPayload
from domain_app.repositories import InMemoryRepository
from domain_app.services import ConsoleNotifier, SuccessReport, EvaluationService
from domain_app.models import GradeBook, Discipline, Student

def main() -> None:
    student_repo = InMemoryRepository[Student]()
    gradebook_repo = InMemoryRepository[GradeBook]()
    
    gradebook = GradeBook(id=1, name="Відомість 2026")
    gradebook_repo.add(gradebook)

    service = EvaluationService(
        gradebook_repo=gradebook_repo,
        student_repo=student_repo,
        notifier=ConsoleNotifier(),
        report_generator=SuccessReport()
    )

    payload_1: StudentPayload = {
        "id": 1,
        "name": "Марія Корхова",
        "group": "ФЕП-33",
        "email": "mariia.korkhova@lnu.edu.ua"
    }
    payload_2: StudentPayload = {
        "id": 2,
        "name": "Іван Петренко",
        "group": "ФЕП-33",
        "email": "ivan.p@example.com"
    }

    s1 = service.register_student(payload_1)
    s2 = service.register_student(payload_2)

    service.assign_student_to_gradebook(s1.id, gradebook.id)
    service.assign_student_to_gradebook(s2.id, gradebook.id)

    oop = Discipline(id=101, name="Професійне ООП", credits=4.0)
    db = Discipline(id=102, name="Бази даних", credits=5.0)

    service.evaluate_student(s1.id, oop, 98.5)
    service.evaluate_student(s1.id, db, 92.0)
    
    service.evaluate_student(s2.id, oop, 74.0)
    service.evaluate_student(s2.id, db, 45.0)

    print("\n--- Аналіз успішності (GradeBook) ---")
    for student in gradebook:
        print(student)
        print(f"  Мін: {student.record.min_score}, Макс: {student.record.max_score}")
        print(f"  Успішність (без боргів): {'Так' if student.record.is_successful else 'Ні'}\n")

    print("--- Сортування за середнім балом (Dunder __lt__) ---")
    for student in gradebook.sort_by_average():
        print(student)

    print("\n--- Фільтрація (вище 90 балів) ---")
    top_students = gradebook.filter_above_threshold(90.0)
    for student in top_students:
        print(f"Відмінник: {student.name}")

    print("\n--- Звіт ---")
    print(service.generate_success_report(gradebook.id))

if __name__ == "__main__":
    main()