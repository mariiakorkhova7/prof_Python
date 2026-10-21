from abc import ABC, abstractmethod
from domain_app.models import Student, Discipline, Grade, GradeBook
from domain_app.value_objects import Score
from domain_app.protocols import Notifier
from domain_app.repositories import InMemoryRepository
from domain_app.dto import StudentPayload

class ReportGenerator(ABC):
    @abstractmethod
    def generate(self, grade_book: GradeBook) -> str:
        pass

class SuccessReport(ReportGenerator):
    def generate(self, grade_book: GradeBook) -> str:
        successful = [s for s in grade_book if s.record.is_successful]
        return f"Успішних студентів (без боргів): {len(successful)} з {len(list(grade_book))}"

class ConsoleNotifier:
    def send(self, recipient: str, message: str) -> None:
        print(f"[Notifier -> {recipient}]: {message}")

class EvaluationService:
    def __init__(
        self,
        gradebook_repo: InMemoryRepository[GradeBook],
        student_repo: InMemoryRepository[Student],
        notifier: Notifier,
        report_generator: ReportGenerator,
    ) -> None:
        self._gradebook_repo = gradebook_repo
        self._student_repo = student_repo
        self._notifier = notifier
        self._report_generator = report_generator

    def register_student(self, payload: StudentPayload) -> Student:
        student = Student(
            id=payload["id"],
            name=payload["name"],
            group=payload["group"],
            email=payload.get("email", "unknown@domain.com")
        )
        self._student_repo.add(student)
        return student

    def assign_student_to_gradebook(self, student_id: int, gradebook_id: int) -> None:
        student = self._student_repo.get(student_id)
        book = self._gradebook_repo.get(gradebook_id)
        if not student or not book:
            raise ValueError("Студент або журнал не знайдено")
        book.add_student(student)

    def evaluate_student(self, student_id: int, discipline: Discipline, score_value: float) -> None:
        student = self._student_repo.get(student_id)
        if not student:
            raise ValueError("Студент не знайдений")
        
        grade = Grade(discipline=discipline, score=Score(score_value))
        student.record.add_grade(grade)
        self._notifier.send(student.email, f"Отримано оцінку {score_value} з '{discipline.name}'")

    def generate_success_report(self, gradebook_id: int) -> str:
        book = self._gradebook_repo.get(gradebook_id)
        if not book:
            return "Журнал не знайдено."
        return self._report_generator.generate(book)