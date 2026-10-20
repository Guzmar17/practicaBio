"""Shared by every test: the repository on the path, a key of the tests' own, the analysis once."""

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# A key for the tests only, set before server.py is imported and reads it. Never a real one.
os.environ.setdefault("ECB_EMERGENCY_KEY", "00" * 32)


@pytest.fixture(scope="session")
def analysis():
    from emergency import pipeline

    return pipeline.run()


@pytest.fixture(scope="session")
def episodes(analysis):
    return analysis.episodes
