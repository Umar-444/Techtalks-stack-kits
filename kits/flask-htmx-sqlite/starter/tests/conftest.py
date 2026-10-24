"""Shared pytest fixtures.

CSRF is disabled here so the functional suite can call routes directly.
test_security.py builds its own app with CSRF enabled, because a suite that
turns a protection off cannot also prove it works.
"""

import os
import tempfile

import pytest

from app import create_app
from app.db import init_db


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    application = create_app({
        "TESTING": True,
        "DATABASE": db_path,
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test-secret-key-32-chars-at-least-abcdef",
    })

    with application.app_context():
        init_db()

    yield application

    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()
