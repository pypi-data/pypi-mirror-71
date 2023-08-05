import os
import sqlite3
from unittest.mock import patch
import inquirer


@patch("os.path.exists")
def test_check_db_FNF(self):
    os.path.exists.value = False
    result = inquirer.check_db("blah")
    assert result is False


@patch("sqlite3.connect")
def test_check_db_SqlDbError(self):
    sqlite3.connect.side_effect = sqlite3.DatabaseError("nope")
    result = inquirer.check_db("blah")
    assert result is False


@patch("sqlite3.connect")
def test_check_db_OperationalError(self):
    sqlite3.connect.side_effect = sqlite3.OperationalError("nope")
    result = inquirer.check_db("blah")
    assert result is False


def BROKEN_test_check_db_WrongDb():
    """ can't get this mocked:
            TypeError: catching classes that do not inherit from BaseException is not allowed
    """
    # sqlite3.connect.value = True
    with patch("inquirer.sqlite3.connect().cursor()") as mocksql:
        mocksql.side_effect = sqlite3.OperationalError
        result = inquirer.check_db("blah")
        assert result is False


def test_check_db_SaulGoodMan():
    """ Works, but really shouldn't ?? """
    result = inquirer.check_db("blah")
    assert result is False
