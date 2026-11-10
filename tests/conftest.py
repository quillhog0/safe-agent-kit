from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
ENFORCEMENT = ROOT / "enforcement"


@pytest.fixture
def repo_root() -> Path:
    return ROOT


@pytest.fixture
def enforcement() -> Path:
    return ENFORCEMENT
