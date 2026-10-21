import json
from collections.abc import Iterable
from pathlib import Path
from grading_importer.exceptions import DataExportError
from grading_importer.models import GradeRecord

def export_grades_json(records: Iterable[GradeRecord], path: Path) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    count = 0
    
    try:
        with temporary.open("w", encoding="utf-8") as file:
            file.write("[\n")
            first = True
            for record in records:
                if not first:
                    file.write(",\n")
                json.dump(record.to_dict(), file, ensure_ascii=False, indent=2)
                first = False
                count += 1
            file.write("\n]\n")
        
        # Atomic replace
        temporary.replace(path)
    except (OSError, TypeError) as error:
        temporary.unlink(missing_ok=True)
        raise DataExportError(f"Не вдалося зберегти експорт у {path}") from error
        
    return count