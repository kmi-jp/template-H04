import pytest

from data.exceptions import *


def test_duplicate_key_error():
    try:
        raise DuplicateKeyError([1, 2, 3, 2, 1])
    except DuplicateKeyError as err:
        assert 1 in err.duplicates
        assert 2 in err.duplicates
        assert len(err.duplicates) == 2


@pytest.mark.parametrize(
    "entity",
    [IndexMismatchError, InvalidDataError, DuplicateKeyError],
)
def test_docstrings(entity):
    assert entity.__doc__ is not None