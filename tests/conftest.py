"""Test doubles for the database connection.

The commands only use conn.cursor() as a context manager, cursor.execute(),
fetchone(), fetchall(), conn.commit() and conn.rollback(), so a small fake
is enough to test the business rules without a running MySQL server.
"""
import pytest


class FakeCursor:
    def __init__(self, conn):
        self.conn = conn

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def execute(self, sql, values=None):
        self.conn.executed.append((sql, values))
        if self.conn.raise_on_execute is not None:
            raise self.conn.raise_on_execute

    def fetchone(self):
        return self.conn.results.pop(0)

    def fetchall(self):
        return self.conn.results.pop(0)


class FakeConnection:
    """Returns the queued results in order, one per fetchone()/fetchall() call."""

    def __init__(self, results=None, raise_on_execute=None):
        self.results = list(results or [])
        self.raise_on_execute = raise_on_execute
        self.executed = []
        self.commits = 0
        self.rollbacks = 0

    def cursor(self):
        return FakeCursor(self)

    def commit(self):
        self.commits += 1

    def rollback(self):
        self.rollbacks += 1


@pytest.fixture
def fake_conn():
    return FakeConnection
