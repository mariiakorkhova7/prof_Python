from typing import Protocol
from .models import AssessmentRecord

class GradeRepository(Protocol):
    def save(self, record: AssessmentRecord) -> bool: ...

class Notifier(Protocol):
    def send(self, message: str) -> None: ...

class GradingService:
    def __init__(self, repo: GradeRepository, notifier: Notifier):
        self.repo = repo
        self.notifier = notifier

    def register_grade(self, record: AssessmentRecord) -> None:
        if self.repo.save(record):
            self.notifier.send(f"Grade {record.grade.value} saved for {record.student.name}")
        else:
            raise RuntimeError("Failed to save grade")

class AsyncReportProvider(Protocol):
    async def fetch_report(self, student_id: int) -> dict: ...

class AsyncReportService:
    def __init__(self, provider: AsyncReportProvider):
        self.provider = provider

    async def generate(self, student_id: int) -> dict:
        data = await self.provider.fetch_report(student_id)
        return {"status": data.get("status", "unknown"), "id": student_id}