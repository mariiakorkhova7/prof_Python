from grades.config import get_pass_threshold

def test_default_threshold(monkeypatch):
    monkeypatch.delenv("PASS_THRESHOLD", raising=False)
    assert get_pass_threshold() == 60.0

def test_custom_threshold(monkeypatch):
    monkeypatch.setenv("PASS_THRESHOLD", "75.5")
    assert get_pass_threshold() == 75.5