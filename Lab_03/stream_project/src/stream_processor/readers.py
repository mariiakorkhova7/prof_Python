import csv
import random
from pathlib import Path
from collections.abc import Iterable, Iterator


def read_lines(path: Path) -> Iterator[str]:
    """Streaming reader: читає файл порядково без завантаження всього файлу в RAM."""
    with path.open("r", encoding="utf-8") as file:
        yield from file


def clean_lines(lines: Iterable[str]) -> Iterator[str]:
    """Generator для очищення потоку від порожніх рядків та пробільних символів."""
    for line in lines:
        cleaned = line.strip()
        if cleaned:
            yield cleaned


def generate_test_dataset(path: Path, count: int, seed: int = 42) -> None:
    """Створює тестовий CSV-файл із заданою кількістю записів (Варіант 7)."""
    random.seed(seed)
    disciplines = (
        "Programming",
        "Algorithms",
        "Databases",
        "Philosophy",
        "Math Analysis",
    )
    names = (
        "anna koval",
        "oleh melnyk",
        "iryna bondar",
        "andrii shevchenko",
        "maria boyko",
        "petro novak",
        "dmytro tkach",
        "olena kravets",
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["student_id", "name", "discipline", "grade"])

        for idx in range(1, count + 1):
            # Кожен 250-й запис робимо навмисно некоректним для перевірки streaming validation
            if idx % 250 == 0:
                writer.writerow([idx, "Invalid Student", "Programming", "error_val"])
            elif idx % 333 == 0:
                writer.writerow([idx, "Out Of Bounds", "Algorithms", 105.5])
            else:
                student_id = (idx % 5000) + 1
                name = f"{random.choice(names)} {student_id}"
                discipline = random.choice(disciplines)
                grade = round(random.uniform(50.0, 100.0), 2)
                writer.writerow([student_id, name, discipline, grade])