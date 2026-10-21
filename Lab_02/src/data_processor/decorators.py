# decorators.py
from functools import wraps
from time import perf_counter

def measure_time(func):
    """Декоратор для оцінки часу виконання функції."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        elapsed = perf_counter() - start
        print(f"[{func.__name__}] виконано за: {elapsed:.8f} с")
        return result
    return wrapper