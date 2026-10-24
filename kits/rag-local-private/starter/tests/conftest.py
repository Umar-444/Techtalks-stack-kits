import os

# Must be set before the app modules are imported: the service reads settings at import time.
os.environ.setdefault("TEST_MODE", "true")
os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("RESTRICT_OUTBOUND_EGRESS", "true")
