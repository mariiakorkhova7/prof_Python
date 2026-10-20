class ApplicationError(Exception):
    """Базовий клас винятків для застосунку."""

class ConfigurationError(ApplicationError):
    """Помилка конфігурації."""

class DataError(ApplicationError):
    """Базова помилка даних."""

class DataImportError(DataError):
    """Помилка читання вхідних даних."""

class RecordValidationError(DataError):
    """Помилка валідації конкретного запису."""
    def __init__(self, message: str, *, line_number: int | None = None, field: str | None = None) -> None:
        super().__init__(message)
        self.line_number = line_number
        self.field = field

class DataExportError(DataError):
    """Помилка збереження вихідних даних."""