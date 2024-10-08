# This is a sample file that can contain any unit tests for your python code.
# You can use your own testing frameworks as part of the tests too.
import pytest
from add import add_fn, increment_by_one_fn
from unittest.mock import MagicMock
from snowflake.snowpark import Session
from snowflake.snowpark.functions import lit
from functools import partial

@pytest.fixture()
def session():
    session = Session.builder.config('local_testing', True).create()
    yield session
    session.close()

# Unit tests for UDF
def test_add_fn():
    assert add_fn(1, 4) == 5

# Unit tests for Stored Procedure
def test_increment_by_one_fn(session):
    assert increment_by_one_fn(session, 3) == 4
