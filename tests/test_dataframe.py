import pytest

from data.index import Index
from data.series import Series
from data.dataframe import DataFrame


@pytest.fixture
def users_data():
    return ["user 1", "user 2", "user 3", "user 4"]


@pytest.fixture
def salaries_data():
    return [20000, 300000, 20000, 50000]


@pytest.fixture
def cash_flow_data():
    return [-100, 10000, -2000, 1100]


@pytest.fixture
def names_data():
    return ["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil"]


def test_dataframe(users_data, salaries_data, names_data, cash_flow_data):
    users = Index(labels=users_data, name="names")

    salaries = Series(values=salaries_data, index=users)
    names = Series(values=names_data, index=users)
    cash_flow = Series(values=cash_flow_data, index=users)

    columns = Index(labels=["names", "salary", "cash flow"])
    data = DataFrame(values=[names, salaries, cash_flow], columns=columns)

    assert data.columns == columns
    assert data.values == [names, salaries, cash_flow]
    assert isinstance(data.values, list)
    assert data.get(key="salary") == salaries
    assert data.get(key="cash flow").max() == 10000
    assert data.get(key="wrong key") == None


def test_empty_dataframe():
    with pytest.raises(ValueError):
        DataFrame(values=[])


def test_empty_columns(users_data, salaries_data, names_data, cash_flow_data):
    users = Index(labels=users_data, name="names")

    salaries = Series(values=salaries_data, index=users)
    names = Series(values=names_data, index=users)
    cash_flow = Series(values=cash_flow_data, index=users)

    data = DataFrame(values=[names, salaries, cash_flow])

    assert data.columns.labels == Index(labels=list(range(3))).labels
    assert data.values == [names, salaries, cash_flow]
    assert data.get(key=1) == salaries
    assert data.get(key=2).max() == 10000


@pytest.mark.parametrize(
    "function",
    [DataFrame, DataFrame.get],
)
def test_docstrings(function):
    assert function.__doc__ is not None
