from grading_importer.exceptions import RecordValidationError
from grading_importer.models import GradeRecord

def parse_record(row: dict[str, str], allowed_disciplines: list[str], *, line_number: int) -> GradeRecord:
    try:
        student_id = int(row["student_id"])
    except (KeyError, TypeError, ValueError) as error:
        raise RecordValidationError("Некоректний student_id", line_number=line_number, field="student_id") from error

    name = row.get("name", "").strip()
    if not name:
        raise RecordValidationError("Ім'я студента порожнє", line_number=line_number, field="name")

    discipline = row.get("discipline", "").strip()
    if discipline not in allowed_disciplines:
        raise RecordValidationError(f"Недозволена дисципліна: {discipline}", line_number=line_number, field="discipline")

    try:
        grade = float(row["grade"])
    except (KeyError, TypeError, ValueError) as error:
        raise RecordValidationError("Некоректна оцінка", line_number=line_number, field="grade") from error

    if not (0 <= grade <= 100):
        raise RecordValidationError("Оцінка має бути від 0 до 100", line_number=line_number, field="grade")

    return GradeRecord(
        student_id=student_id,
        name=name,
        discipline=discipline,
        grade=grade,
    )