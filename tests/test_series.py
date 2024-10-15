import statistics
import pytest

from data.index import Index
from data.series import Series


@pytest.fixture
def values_data():
    return [20000, 300000, 20000, 50000]


@pytest.fixture
def idx():
    return Index(labels=["user 1", "user 2", "user 3", "user 4"], name="names")


def test_series(values_data, idx):
    values = values_data

    salaries = Series(values=values, index=idx)

    assert salaries.values == values
    assert isinstance(salaries.values, list)
    assert salaries.index == idx


def test_empty_index(values_data):
    salaries = Series(values=values_data)

    assert salaries.index.labels == Index(labels=list(range(len(values_data)))).labels


def test_series_get(values_data, idx):
    salaries = Series(values=values_data, index=idx)

    assert salaries.get(key="user 2") == values_data[1]
    assert salaries.get(key="wrong key") == None


def test_series_sum(values_data, idx):
    salaries = Series(values=values_data, index=idx)

    assert salaries.sum() == sum(values_data)


def test_series_max(values_data, idx):
    salaries = Series(values=values_data, index=idx)

    assert salaries.max() == max(values_data)


def test_series_min(values_data, idx):
    salaries = Series(values=values_data, index=idx)

    assert salaries.min() == min(values_data)


def test_series_mean(values_data, idx):
    salaries = Series(values=values_data, index=idx)

    assert salaries.mean() == statistics.mean(values_data)


def test_series_apply(values_data, idx):
    salaries = Series(values=values_data, index=idx)

    def squared(a):
        """Returns squared number"""
        return a ** 2

    result = salaries.apply(func=squared)

    assert salaries != result
    assert salaries is not result
    assert result.values == list(map(squared, values_data))


def test_series_abs(idx):
    values = [20000, -300000, 20000, -50000]

    salaries = Series(values=values, index=idx)

    result = salaries.abs()

    assert salaries != result
    assert salaries is not result
    assert result.values == list(map(abs, values))


def test_empty_series():
    with pytest.raises(ValueError):
        Series(values=[])


@pytest.mark.parametrize(
    "values,labels",
    [
        ([20000, 300000, 20000], ["user 1"]),
        ([20000], ["user 1", "user 2"]),
    ],
)
def test_values_index_length_mismatch(values, labels):
    idx = Index(labels, name="names")

    with pytest.raises(ValueError):
        Series(values=values, index=idx)


@pytest.mark.parametrize(
    "function",
    [
        Series,
        Series.get,
        Series.sum,
        Series.max,
        Series.min,
        Series.mean,
        Series.apply,
        Series.abs,
    ],
)
def test_docstrings(function):
    assert function.__doc__ is not None
