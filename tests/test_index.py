import pytest

from data.index import Index


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
    with pytest.raises(ValueError):
        Index(labels=[])


def test_nonempty_name(keys):
    idx = Index(labels=keys, name="index")

    assert idx.name == "index"


def test_invalid_key():
    with pytest.raises(KeyError):
        Index(labels=["key 1"]).get_loc(key="key 2")


def test_label_duplicity():
    with pytest.raises(ValueError):
        Index(labels=["key 1", "key 1", "key 3", "key 4", "key 5"])


@pytest.mark.parametrize(
    "function",
    [Index, Index.get_loc],
)
def test_docstrings(function):
    assert function.__doc__ is not None
