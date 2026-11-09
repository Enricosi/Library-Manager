from argparse import Namespace

import pymysql
import pytest

from commands_book import cmd_add_book, cmd_remove_book
from commands_copy import cmd_change_copy_status, cmd_remove_copy
from commands_loan import cmd_list_loans, cmd_loan_copy, cmd_return_copy
from commands_users import cmd_change_user_activity, cmd_list_users
from dispatch import dispatch
from exceptions import LibraryManagerError


def test_unknown_command_raises(fake_conn):
    with pytest.raises(RuntimeError):
        dispatch(Namespace(command="nope"), fake_conn())


def test_duplicate_isbn_rolls_back(fake_conn):
    conn = fake_conn(raise_on_execute=pymysql.err.IntegrityError())
    args = Namespace(title="1984", author="George Orwell", genre="Dystopia", year=None, isbn="123")
    with pytest.raises(LibraryManagerError):
        cmd_add_book(args, conn)
    assert conn.rollbacks == 1


def test_book_with_copies_cannot_be_removed(fake_conn):
    conn = fake_conn(results=[(1,), (10,)])
    with pytest.raises(LibraryManagerError):
        cmd_remove_book(Namespace(id=1), conn)
    assert conn.commits == 0


def test_loaned_copy_cannot_be_removed(fake_conn):
    conn = fake_conn(results=[("loaned",)])
    with pytest.raises(LibraryManagerError):
        cmd_remove_copy(Namespace(id=3), conn)


def test_lost_copy_cannot_become_damaged(fake_conn):
    conn = fake_conn(results=[(3,), ("lost",)])
    with pytest.raises(LibraryManagerError):
        cmd_change_copy_status(Namespace(copy=3, new_status="damaged"), conn)
    assert conn.commits == 0


def test_damaging_a_loaned_copy_closes_its_loan(fake_conn):
    conn = fake_conn(results=[(3,), ("loaned",), (42,)])
    cmd_change_copy_status(Namespace(copy=3, new_status="damaged"), conn)
    statements = [sql for sql, _ in conn.executed]
    assert any(sql.startswith("UPDATE loan SET return_date") for sql in statements)
    assert conn.executed[-1] == ("UPDATE copy SET status = %s WHERE copy_id = %s", ("damaged", 3))
    assert conn.commits == 1


def test_unavailable_copy_cannot_be_loaned(fake_conn):
    conn = fake_conn(results=[("damaged",)])
    with pytest.raises(LibraryManagerError):
        cmd_loan_copy(Namespace(id=3, username="jdoe", days=14), conn)


def test_inactive_user_cannot_borrow(fake_conn):
    conn = fake_conn(results=[("available",), (8,), (0,)])
    with pytest.raises(LibraryManagerError):
        cmd_loan_copy(Namespace(id=3, username="jdoe", days=14), conn)
    assert conn.commits == 0


def test_loan_creates_loan_and_marks_copy_loaned(fake_conn):
    conn = fake_conn(results=[("available",), (8,), (1,)])
    cmd_loan_copy(Namespace(id=3, username="jdoe", days=14), conn)
    insert_sql, insert_values = conn.executed[-2]
    assert insert_sql.startswith("INSERT INTO loan")
    copy_id, user_id, loan_date, due_date = insert_values
    assert (copy_id, user_id) == (3, 8)
    assert (due_date - loan_date).days == 14
    assert conn.executed[-1][0].startswith("UPDATE copy SET status = 'loaned'")
    assert conn.commits == 1


def test_returning_a_copy_that_is_not_loaned_raises(fake_conn):
    conn = fake_conn(results=[("available",)])
    with pytest.raises(LibraryManagerError):
        cmd_return_copy(Namespace(copy=3), conn)


def test_user_with_active_loan_cannot_be_deactivated(fake_conn):
    conn = fake_conn(results=[(8,), (1,), (None,)])
    with pytest.raises(LibraryManagerError):
        cmd_change_user_activity(Namespace(user="jdoe"), conn)
    assert conn.commits == 0


def test_active_and_inactive_filters_are_exclusive(fake_conn):
    with pytest.raises(LibraryManagerError):
        cmd_list_users(Namespace(active=True, inactive=True, have_loans=False), fake_conn())


def test_active_and_historical_loans_are_exclusive(fake_conn):
    with pytest.raises(LibraryManagerError):
        cmd_list_loans(Namespace(active=True, historical=True), fake_conn())
