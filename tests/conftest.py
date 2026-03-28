"""
Pytest configuration for the test suite.
"""

from pathlib import Path
import pytest

@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """
    Fixture that provides the path to the test data directory.
    """
    return Path(__file__).parent / "data"
