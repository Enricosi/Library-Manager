import argparse
import sys

import pytest

from parser import parse_args, valid_days


@pytest.mark.parametrize("days", ["1", "14", "60"])
def test_valid_days_accepts_range(days):
    assert valid_days(days) == int(days)


@pytest.mark.parametrize("days", ["0", "61", "-3"])
def test_valid_days_rejects_out_of_range(days):
    with pytest.raises(argparse.ArgumentTypeError):
        valid_days(days)


def parse(monkeypatch, *argv):
    monkeypatch.setattr(sys, "argv", ["library_manager.py", *argv])
    return parse_args()


def test_loan_copy(monkeypatch):
    args = parse(monkeypatch, "loan_copy", "5", "jdoe", "14")
    assert (args.command, args.id, args.username, args.days) == ("loan_copy", 5, "jdoe", 14)


def test_copy_cannot_be_set_to_loaned_from_cli(monkeypatch):
    with pytest.raises(SystemExit):
        parse(monkeypatch, "change_copy_status", "5", "loaned")
