import subprocess
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "enforcement" / "ast_gate.py"


def run(*files):
    return subprocess.run(
        ["python3", str(SCRIPT), *files],
        capture_output=True,
        text=True,
    )


def test_identical_files_pass(tmp_path):
    src = tmp_path / "a.py"
    src.write_text("def add(x, y):\n    return x + y\n")
    other = tmp_path / "b.py"
    other.write_text(src.read_text())
    result = run(str(src), str(other))
    assert result.returncode == 0, result.stderr
    assert "pass" in result.stdout


def test_comment_only_change_passes(tmp_path):
    original = tmp_path / "original.py"
    modified = tmp_path / "modified.py"
    original.write_text("x = 1  # old note\n")
    modified.write_text("x = 1  # new note\n")
    result = run(str(original), str(modified))
    assert result.returncode == 0, result.stderr


def test_docstring_only_change_passes(tmp_path):
    original = tmp_path / "original.py"
    modified = tmp_path / "modified.py"
    original.write_text('def f():\n    """old"""\n    return 1\n')
    modified.write_text('def f():\n    """new"""\n    return 1\n')
    result = run(str(original), str(modified))
    assert result.returncode == 0, result.stderr


def test_code_change_fails(tmp_path):
    original = tmp_path / "original.py"
    modified = tmp_path / "modified.py"
    original.write_text("x = 1\n")
    modified.write_text("x = 2\n")
    result = run(str(original), str(modified))
    assert result.returncode == 1
    assert "differ" in result.stderr


def test_syntax_error_fails(tmp_path):
    original = tmp_path / "original.py"
    modified = tmp_path / "modified.py"
    original.write_text("x = 1\n")
    modified.write_text("def (\n")
    result = run(str(original), str(modified))
    assert result.returncode == 1
    assert "Syntax error" in result.stderr


def test_non_python_rejected(tmp_path):
    ts = tmp_path / "a.ts"
    py = tmp_path / "a.py"
    ts.write_text("const x = 1;\n")
    py.write_text("x = 1\n")
    result = run(str(ts), str(py))
    assert result.returncode == 2
    assert "Python" in result.stderr


def test_usage_without_args():
    result = run()
    assert result.returncode == 2
    assert "Usage" in result.stderr


def test_missing_file(tmp_path):
    existing = tmp_path / "a.py"
    existing.write_text("x = 1\n")
    result = run(str(existing), str(tmp_path / "missing.py"))
    assert result.returncode == 1
    assert "Cannot read file" in result.stderr
