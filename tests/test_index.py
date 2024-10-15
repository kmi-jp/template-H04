import pytest

from data.index import Index
from data.exceptions import InvalidDataError, DuplicateKeyError


@pytest.fixture
def keys():
    return ["key 1", "key 2", "key 3", "key 4", "key 5"]


def test_index(keys):
    idx = Index(labels=keys)
    values = [0, 1, 2, 3, 4]

    assert idx.labels == keys
    assert isinstance(idx.labels, list)
    assert values[idx.get_loc(key="key 2")] == 1
    assert idx.name == ""


def test_empty_labels():
    with pytest.raises(InvalidDataError):
        Index(labels=[])


def test_nonempty_name(keys):
    idx = Index(labels=keys, name="index")

    assert idx.name == "index"


def test_invalid_key():
    with pytest.raises(KeyError):
        Index(labels=["key 1"]).get_loc(key="key 2")


def test_label_duplicity():
    with pytest.raises(DuplicateKeyError) as err:
        Index(labels=["key 1", "key 3", "key 4", "key 1", "key 5"]) 

    assert len(err.value.duplicates) == 1
    assert "key 1" in err.value.duplicates
        

@pytest.mark.parametrize(
    "function",
    [Index, Index.get_loc],
)
def test_docstrings(function):
    assert function.__doc__ is not None
