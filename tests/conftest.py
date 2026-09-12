"""
Root test runner configuration and fixtures.
"""

import sys
from pathlib import Path
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "backend"))

@pytest.fixture(scope="session")
def project_root():
    return ROOT_DIR
