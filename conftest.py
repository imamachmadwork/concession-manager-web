from pathlib import Path

import allure
import pytest
from dotenv import load_dotenv

load_dotenv()


def pytest_collection_modifyitems(items):
    """Auto-tag every test as frontend (tests/e2e) or backend (tests/api),
    so suites can be run/filtered independently with `pytest -m frontend`."""
    for item in items:
        parts = Path(str(item.fspath)).parts
        if "e2e" in parts:
            item.add_marker(pytest.mark.frontend)
        elif "api" in parts:
            item.add_marker(pytest.mark.backend)


@pytest.fixture(autouse=True)
def _allure_suite_labels(request):
    """Tag every test with an Allure epic (suite) and feature (layer), so the
    Allure report can be sliced by test suite or by Frontend/Backend without
    per-test decorators.

    - epic: derived from the test file name, e.g. test_sign_in.py -> "Sign In"
    - feature: "Frontend" for tests/e2e, "Backend" for tests/api
    """
    path = Path(str(request.node.fspath))
    allure.dynamic.epic(path.stem.removeprefix("test_").replace("_", " ").title())

    parts = path.parts
    if "e2e" in parts:
        allure.dynamic.feature("Frontend")
    elif "api" in parts:
        allure.dynamic.feature("Backend")
