import importlib.util
import subprocess
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "enforcement" / "validate_report.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_report", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALID = """STATUS: HANDED_TO_REVIEW
CHANGED: src/invoice.py — extracted is_in_grace()
VERIFIED: pytest -q → 3 passed
NOT DONE / SKIPPED: none
RISKS: none
HALT_CHECKED: yes
RULE_FILES_TOUCHED: no
QUESTIONS FOR Alice: none
"""


def write_report(tmp_path, text):
    path = tmp_path / "report.md"
    path.write_text(text)
    return path


def run_cli(path):
    return subprocess.run(
        ["python3", str(SCRIPT), str(path)],
        capture_output=True,
        text=True,
    )


def test_valid_report_passes(tmp_path):
    path = write_report(tmp_path, VALID)
    result = run_cli(path)
    assert result.returncode == 0, result.stderr
    assert "valid" in result.stdout


def test_banner_above_fields_is_allowed(tmp_path):
    text = "> Illustrative example only.\n\n" + VALID
    result = run_cli(write_report(tmp_path, text))
    assert result.returncode == 0, result.stderr


def test_missing_status_fails(tmp_path):
    text = "\n".join(line for line in VALID.splitlines() if not line.startswith("STATUS:"))
    result = run_cli(write_report(tmp_path, text + "\n"))
    assert result.returncode == 1
    assert "STATUS" in result.stderr


def test_invalid_status_fails(tmp_path):
    text = VALID.replace("STATUS: HANDED_TO_REVIEW", "STATUS: SHIPPED")
    result = run_cli(write_report(tmp_path, text))
    assert result.returncode == 1
    assert "STATUS" in result.stderr


def test_empty_changed_fails(tmp_path):
    text = VALID.replace("CHANGED: src/invoice.py — extracted is_in_grace()", "CHANGED:")
    result = run_cli(write_report(tmp_path, text))
    assert result.returncode == 1
    assert "CHANGED" in result.stderr


def test_empty_verified_fails(tmp_path):
    text = VALID.replace("VERIFIED: pytest -q → 3 passed", "VERIFIED:   ")
    result = run_cli(write_report(tmp_path, text))
    assert result.returncode == 1
    assert "VERIFIED" in result.stderr


def test_invalid_halt_checked_fails(tmp_path):
    text = VALID.replace("HALT_CHECKED: yes", "HALT_CHECKED: maybe")
    result = run_cli(write_report(tmp_path, text))
    assert result.returncode == 1
    assert "HALT_CHECKED" in result.stderr


def test_invalid_rule_files_touched_fails(tmp_path):
    text = VALID.replace("RULE_FILES_TOUCHED: no", "RULE_FILES_TOUCHED: unknown")
    result = run_cli(write_report(tmp_path, text))
    assert result.returncode == 1
    assert "RULE_FILES_TOUCHED" in result.stderr


def test_missing_questions_for_fails(tmp_path):
    text = "\n".join(line for line in VALID.splitlines() if not line.startswith("QUESTIONS FOR"))
    result = run_cli(write_report(tmp_path, text + "\n"))
    assert result.returncode == 1
    assert "QUESTIONS FOR" in result.stderr


def test_missing_risks_fails(tmp_path):
    text = "\n".join(line for line in VALID.splitlines() if not line.startswith("RISKS:"))
    result = run_cli(write_report(tmp_path, text + "\n"))
    assert result.returncode == 1
    assert "RISKS" in result.stderr


def test_halt_checked_na_allowed(tmp_path):
    text = VALID.replace("HALT_CHECKED: yes", "HALT_CHECKED: n/a")
    result = run_cli(write_report(tmp_path, text))
    assert result.returncode == 0, result.stderr


def test_multiline_changed_is_non_empty(tmp_path):
    text = VALID.replace(
        "CHANGED: src/invoice.py — extracted is_in_grace()",
        "CHANGED:\n  src/invoice.py — extracted is_in_grace()\n  src/tests/test_invoice.py — added cases",
    )
    result = run_cli(write_report(tmp_path, text))
    assert result.returncode == 0, result.stderr


def test_usage_without_args():
    result = subprocess.run(["python3", str(SCRIPT)], capture_output=True, text=True)
    assert result.returncode == 2


def test_validator_function_lists_all_missing():
    module = load_validator()
    errors = module.validate("hello\n")
    keys = [e.split(": ", 1)[-1] for e in errors if e.startswith("missing field:")]
    assert "STATUS" in keys
    assert "HALT_CHECKED" in keys
    assert "QUESTIONS FOR" in keys
