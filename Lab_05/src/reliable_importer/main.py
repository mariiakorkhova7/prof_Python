import logging
from pathlib import Path

from grading_importer.config import load_config
from grading_importer.exceptions import ApplicationError
from grading_importer.exporters import export_grades_json
from grading_importer.logging_config import configure_logging
from grading_importer.services import (
    ImportStatistics,
    filter_by_passing_grade,
    import_grades,
    logged_operation,
)

logger = logging.getLogger(__name__)

def main() -> None:
    try:
        config = load_config(Path("config.yaml"))
        configure_logging(config.logging.level, config.logging.path)
        statistics = ImportStatistics()

        with logged_operation("Grade import/export"):
            records = import_grades(
                config.input_path,
                allowed_disciplines=config.processing.allowed_disciplines,
                skip_invalid=config.processing.skip_invalid,
                statistics=statistics,
            )
            
            passed_records = filter_by_passing_grade(
                records,
                config.processing.passing_grade,
            )
            
            exported = export_grades_json(passed_records, config.output_path)
            
        logger.info(
            "Total=%s, valid=%s, invalid=%s, exported=%s",
            statistics.total,
            statistics.valid,
            statistics.invalid,
            exported,
        )
    except ApplicationError as error:
        logger.error("Application error: %s", error)
        raise SystemExit(1) from error

if __name__ == "__main__":
    main()