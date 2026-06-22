import pytest
from runbook import Runbook, Version, Step

def test_add_version():
    runbook = Runbook("Test Runbook")
    version = Version("2022-01-01 12:00:00", "John Doe", [Step("Step 1"), Step("Step 2")])
    runbook.add_version(version)
    assert len(runbook.get_versions()) == 1

def test_diff_versions():
    runbook = Runbook("Test Runbook")
    version1 = Version("2022-01-01 12:00:00", "John Doe", [Step("Step 1"), Step("Step 2")])
    version2 = Version("2022-01-02 12:00:00", "Jane Doe", [Step("Step 1"), Step("Step 3")])
    runbook.add_version(version1)
    runbook.add_version(version2)
    added_steps, removed_steps = runbook.diff_versions(version1, version2)
    assert len(added_steps) == 1
    assert len(removed_steps) == 1

def test_search():
    runbook = Runbook("Test Runbook")
    version = Version("2022-01-01 12:00:00", "John Doe", [Step("Step 1"), Step("Step 2")])
    runbook.add_version(version)
    results = runbook.search("Step 1")
    assert len(results) == 1

def test_search_no_results():
    runbook = Runbook("Test Runbook")
    version = Version("2022-01-01 12:00:00", "John Doe", [Step("Step 1"), Step("Step 2")])
    runbook.add_version(version)
    results = runbook.search("Step 3")
    assert len(results) == 0
