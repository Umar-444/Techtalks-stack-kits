import os
import sys

# Tests import `main` from the starter root regardless of where pytest is run.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


import copy

import pytest


@pytest.fixture(autouse=True)
def _reset_state():
    """The API keeps users and rate counters in module globals; isolate each test."""
    import main

    snapshot = copy.deepcopy(main.USER_PROFILES)
    main.RATE_LIMIT_STORE.clear()
    yield
    main.RATE_LIMIT_STORE.clear()
    main.USER_PROFILES.clear()
    main.USER_PROFILES.update(snapshot)
