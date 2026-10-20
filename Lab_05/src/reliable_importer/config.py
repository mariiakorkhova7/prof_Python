import yaml
from pathlib import Path

from grading_importer.exceptions import ConfigurationError
from grading_importer.models import AppConfig, LoggingConfig, ProcessingConfig

def load_config(path: Path) -> AppConfig:
    try:
        with path.open("r", encoding="utf-8") as file:
            raw = yaml.safe_load(file)
    except FileNotFoundError as error:
        raise ConfigurationError(f"Файл конфігурації не знайдено: {path}") from error
    except yaml.YAMLError as error:
        raise ConfigurationError("Невалідний YAML файл") from error

    try:
        config = AppConfig(
            input_path=Path(raw["input"]["path"]),
            output_path=Path(raw["output"]["path"]),
            processing=ProcessingConfig(
                allowed_disciplines=list(raw["processing"]["allowed_disciplines"]),
                passing_grade=float(raw["processing"]["passing_grade"]),
                skip_invalid=bool(raw["processing"]["skip_invalid"]),
            ),
            logging=LoggingConfig(
                level=str(raw["logging"]["level"]),
                path=Path(raw["logging"]["path"]),
            ),
        )
    except (KeyError, TypeError, ValueError) as error:
        raise ConfigurationError("Структура конфігурації некоректна") from error

    validate_config(config)
    return config

def validate_config(config: AppConfig) -> None:
    if not (0 <= config.processing.passing_grade <= 100):
        raise ConfigurationError("passing_grade повинно бути між 0 та 100")
    if not config.processing.allowed_disciplines:
        raise ConfigurationError("allowed_disciplines не може бути порожнім списком")
    if not config.input_path.exists():
        raise ConfigurationError(f"Вхідний файл не знайдено: {config.input_path}")