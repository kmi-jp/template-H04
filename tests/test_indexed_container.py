import pytest


from data.index import Index
from data.series import Series
from data.indexed_container import IndexedContainer
from data.exceptions import IndexMismatchError, InvalidDataError

@pytest.fixture
def values_data():
    return [20000, 300000, 20000, 50000]


@pytest.fixture
def idx():
    return Index(labels=["user 1", "user 2", "user 3", "user 4"], name="names")


def test_empty_index(values_data):
    salaries = IndexedContainer(values=values_data)

    assert salaries.index.labels == Index(labels=list(range(len(values_data)))).labels


def test_empty_indexed_container():
    with pytest.raises(InvalidDataError):
        IndexedContainer(values=[])


@pytest.mark.parametrize(
    "values,labels",
    [
        ([20000, 300000, 20000], ["user 1"]),
        ([20000], ["user 1", "user 2"]),
    ],
)
def test_values_mismatch_indexed_container_length(values, labels):
    idx = Index(labels, name="names")

    with pytest.raises(IndexMismatchError):
        IndexedContainer(values=values, index=idx)


def test_indexed_container_get(values_data, idx):
    salaries = IndexedContainer(values=values_data, index=idx)

    assert salaries.get(key="user 2") == values_data[1]
    assert salaries.get(key="wrong key") == None


@pytest.mark.parametrize(
    "function",
    [IndexedContainer, IndexedContainer.get],
)
def test_docstrings(function):
    assert function.__doc__ is not None

