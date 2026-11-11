"""Demonstrate one pytest retry for a simulated transient failure.

Run from the repository root with:
    python -m pytest -v retry_demo.py

This demo requires the pytest-rerunfailures plugin.
"""

import pytest


_attempt_count = 0


@pytest.mark.flaky(reruns=1)
def test_passes_after_one_retry():
    """Fail once, then pass when pytest-rerunfailures reruns this test."""
    global _attempt_count
    _attempt_count += 1

    assert _attempt_count > 1, "Simulated transient failure on the first attempt"
