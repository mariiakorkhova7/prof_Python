from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Score:
    value: float

    def __post_init__(self) -> None:
        if not (0.0 <= self.value <= 100.0):
            raise ValueError("Оцінка повинна бути в діапазоні від 0 до 100")

    def __str__(self) -> str:
        return f"{self.value:.1f}"