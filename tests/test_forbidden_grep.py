import os
import stat
import subprocess
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "enforcement" / "forbidden_grep.sh"


def run(args, cwd, env=None, pattern_as_arg=True):
    full_env = os.environ.copy()
    if env:
        full_env.update(env)
    return subprocess.run(
        ["bash", str(SCRIPT), *args],
        cwd=cwd,
        env=full_env,
        capture_output=True,
        text=True,
    )


def test_fails_closed_without_pattern(tmp_path):
    (tmp_path / "ok.txt").write_text("nothing sensitive\n")
    result = run([], cwd=tmp_path, env={"FORBIDDEN_PATTERNS_GREP": ""})
    assert result.returncode == 2, result.stderr
    assert "fail closed" in result.stderr
    assert "no pattern" in result.stderr.lower() or "no pattern configured" in result.stderr


def test_fails_closed_when_env_unset(tmp_path, monkeypatch):
    env = os.environ.copy()
    env.pop("FORBIDDEN_PATTERNS_GREP", None)
    result = subprocess.run(
        ["bash", str(SCRIPT)],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2, result.stderr


def test_finds_pattern(tmp_path):
    (tmp_path / "leak.txt").write_text("account acct_live_123 is here\n")
    result = run(["acct_live_"], cwd=tmp_path)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "Forbidden pattern found" in result.stderr
    assert "acct_live_" in result.stdout


def test_clean_when_no_match(tmp_path):
    (tmp_path / "ok.txt").write_text("synthetic_id_001\n")
    result = run(["acct_live_|broker.prod.com"], cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert "clean" in result.stdout


def test_skips_archive_directory(tmp_path):
    archived = tmp_path / "_archive" / "old.txt"
    archived.parent.mkdir()
    archived.write_text("acct_live_should_be_ignored\n")
    (tmp_path / "ok.txt").write_text("fine\n")
    result = run(["acct_live_"], cwd=tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr


def test_pattern_from_env(tmp_path):
    (tmp_path / "leak.txt").write_text("secret-host.example\n")
    result = run([], cwd=tmp_path, env={"FORBIDDEN_PATTERNS_GREP": "secret-host\\.example"})
    assert result.returncode == 1, result.stdout + result.stderr


def test_custom_path_argument(tmp_path):
    watched = tmp_path / "src"
    ignored = tmp_path / "other"
    watched.mkdir()
    ignored.mkdir()
    (watched / "a.txt").write_text("clean\n")
    (ignored / "b.txt").write_text("acct_live_only_here\n")
    result = run(["acct_live_", str(watched)], cwd=tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
