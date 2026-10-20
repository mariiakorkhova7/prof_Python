from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass(frozen=True, slots=True)
class GradeRecord:
    student_id: int
    name: str
    discipline: str
    grade: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

@dataclass(frozen=True, slots=True)
class ProcessingConfig:
    allowed_disciplines: list[str]
    passing_grade: float
    skip_invalid: bool

@dataclass(frozen=True, slots=True)
class LoggingConfig:
    level: str
    path: Path

@dataclass(frozen=True, slots=True)
class AppConfig:
    input_path: Path
    output_path: Path
    processing: ProcessingConfig
    logging: LoggingConfig