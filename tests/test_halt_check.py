import os
import subprocess
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "enforcement" / "halt_check.sh"


def run(args, cwd, env=None):
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


def test_absent_halt_file_passes(tmp_path):
    result = run([str(tmp_path / "state" / "HALT")], cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert "HALT_CHECKED: yes" in result.stdout


def test_existing_halt_file_fails(tmp_path):
    halt = tmp_path / "HALT"
    halt.write_text("stopped\n")
    result = run([str(halt)], cwd=tmp_path)
    assert result.returncode == 1
    assert "blocked" in result.stdout.lower() or "blocked" in result.stderr.lower()
    assert str(halt) in result.stdout or str(halt) in result.stderr


def test_env_var_path(tmp_path):
    halt = tmp_path / "custom.HALT"
    halt.write_text("x\n")
    result = run([], cwd=tmp_path, env={"HALT_FILE": str(halt)})
    assert result.returncode == 1


def test_default_path_absent_from_empty_dir(tmp_path):
    result = run([], cwd=tmp_path, env={"HALT_FILE": "state/HALT"})
    assert result.returncode == 0, result.stderr
