import math
import random
from functools import lru_cache
from typing import Dict, List, Tuple
import numpy as np


def generate_grades(count: int, seed: int = 42) -> List[float]:
    """Генерація масиву оцінок від 60.0 до 100.0 (1,000,000+ для Варіанта 7)."""
    random.seed(seed)
    return [random.uniform(60.0, 100.0) for _ in range(count)]


def statistics_python(values: List[float]) -> Dict[str, float]:
    """Baseline реалізація статистики на чистих циклах Python."""
    count = len(values)
    if count == 0:
        return {"average": 0.0, "minimum": 0.0, "maximum": 0.0, "std": 0.0}

    avg = sum(values) / count
    minimum = min(values)
    maximum = max(values)

    variance = sum((v - avg) ** 2 for v in values) / count
    std_dev = math.sqrt(variance)

    return {
        "average": avg,
        "minimum": minimum,
        "maximum": maximum,
        "std": std_dev,
    }


def statistics_numpy(values: List[float]) -> Dict[str, float]:
    """Векторизована реалізація за допомогою NumPy."""
    array = np.asarray(values, dtype=np.float64)
    if array.size == 0:
        return {"average": 0.0, "minimum": 0.0, "maximum": 0.0, "std": 0.0}

    return {
        "average": float(array.mean()),
        "minimum": float(array.min()),
        "maximum": float(array.max()),
        "std": float(array.std()),
    }


def heavy_grade_score(grade: float) -> float:
    """CPU-bound обчислення складного трансформованого коефіцієнта оцінки."""
    val = grade
    for _ in range(80):
        val = math.sin(val) ** 2 + math.cos(val) ** 2 + math.sqrt(abs(val) + 1.0)
    return val


def calculate_scores_sequential(grades: List[float]) -> List[float]:
    return [heavy_grade_score(g) for g in grades]


@lru_cache(maxsize=128)
def cached_discipline_statistics(discipline_name: str, repo_version: int, values_tuple: Tuple[float, ...]) -> Dict[str, float]:
    """
    Кешована статистика з підтримкою Cache Invalidation через repo_version.
    """
    return statistics_numpy(list(values_tuple))