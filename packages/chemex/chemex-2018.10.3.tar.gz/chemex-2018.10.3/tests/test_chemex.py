"""Unit and regression test for the chemex package."""
import sys

import chemex  # noqa: F401; pylint: disable=unused-variable


def test_chemex_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "chemex" in sys.modules
