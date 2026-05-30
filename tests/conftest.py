"""
tests/conftest.py

Pytest configuration and session-level fixtures.
Verifies that the Flask server is reachable before running any tests.
"""

import pytest
import requests


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "smoke: mark test as part of the smoke test suite"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as a regression test"
    )
    config.addinivalue_line(
        "markers", "negative: mark test as a negative/error-path test"
    )


def pytest_sessionstart(session):
    """Check server availability before the test session begins."""
    try:
        r = requests.get("http://localhost:5000/health", timeout=3)
        if r.status_code != 200:
            raise RuntimeError("Server responded but health check failed.")
        print("\n✅  Server is up — starting test suite\n")
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "\n❌  Could not connect to http://localhost:5000\n"
            "    Please start the Flask server first:\n"
            "      python app.py\n"
        )
