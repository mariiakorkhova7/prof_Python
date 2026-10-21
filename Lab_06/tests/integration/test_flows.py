import pytest
import json
from grades.io import read_csv, write_json, DataImportError
from grades.book import GradeBook
from grades.config import get_pass_threshold

@pytest.fixture
def tmp_valid_csv(tmp_path):
    path = tmp_path / "valid.csv"
    path.write_text(
        "student_id,student_name,discipline_id,discipline_name,grade\n"
        "1,Anna,10,Math,95\n"
        "2,Oleh,10,Math,55\n", 
        encoding="utf-8"
    )
    return path

@pytest.fixture
def tmp_invalid_csv(tmp_path):
    path = tmp_path / "invalid.csv"
    path.write_text(
        "student_id,student_name,discipline_id,discipline_name,grade\n"
        "1,Anna,10,Math,150\n", 
        encoding="utf-8"
    )
    return path

@pytest.mark.integration
def test_import_filter_export_flow(tmp_valid_csv, tmp_path, monkeypatch):
    monkeypatch.setenv("PASS_THRESHOLD", "60.0")
    
    # 1. Import
    records = list(read_csv(tmp_valid_csv))
    book = GradeBook(records)
    
    # 2. Filter using config
    threshold = get_pass_threshold()
    passed = book.get_students_above_threshold(threshold)
    
    # 3. Export
    out_json = tmp_path / "passed.json"
    write_json(passed, out_json)
    
    # 4. Verify
    assert out_json.exists()
    data = json.loads(out_json.read_text(encoding="utf-8"))
    assert len(data) == 1
    assert data[0]["name"] == "Anna"
    assert data[0]["grade"] == 95.0

@pytest.mark.integration
def test_csv_import_malformed_record(tmp_invalid_csv):
    with pytest.raises(DataImportError, match="Malformed record"):
        list(read_csv(tmp_invalid_csv))