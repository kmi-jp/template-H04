import pytest

from data.index import Index
from data.series import Series
from data.dataframe import DataFrame
from data.indexed_container import IndexedContainer
from data.exceptions import InvalidDataError


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

    index = Index(labels=["names", "salary", "cash flow"])
    data = DataFrame(values=[names, salaries, cash_flow], index=index)

    assert data.index == index
    assert data.values == [names, salaries, cash_flow]
    assert isinstance(data.values, list)
    assert data.get(key="salary") == salaries
    assert data.get(key="cash flow").max() == 10000
    assert data.get(key="wrong key") == None
    assert isinstance(data, IndexedContainer)


def test_dataframe_parent_class(users_data, salaries_data, names_data, cash_flow_data):
    users = Index(labels=users_data, name="names")

    salaries = Series(values=salaries_data, index=users)
    names = Series(values=names_data, index=users)
    cash_flow = Series(values=cash_flow_data, index=users)

    index = Index(labels=["names", "salary", "cash flow"])
    data = DataFrame(values=[names, salaries, cash_flow], index=index)

    assert isinstance(data, IndexedContainer) == True
    assert isinstance(data, Series) == False
    assert isinstance(data, Index) == False


def test_dataframe_valuues(users_data, salaries_data, names_data, cash_flow_data):
    users = Index(labels=users_data, name="names")

    salaries = Series(values=salaries_data, index=users)
    names = Series(values=names_data, index=users)
    cash_flow = Series(values=cash_flow_data, index=users)

    index = Index(labels=["names", "salary", "cash flow"])

    with pytest.raises(InvalidDataError):
        DataFrame(values=[salaries, names, 42, cash_flow], index=index)


def test_empty_dataframe():
    with pytest.raises(InvalidDataError):
        DataFrame(values=[])


def test_empty_index(users_data, salaries_data, names_data, cash_flow_data):
    users = Index(labels=users_data, name="names")

    salaries = Series(values=salaries_data, index=users)
    names = Series(values=names_data, index=users)
    cash_flow = Series(values=cash_flow_data, index=users)

    data = DataFrame(values=[names, salaries, cash_flow])

    assert data.index.labels == Index(labels=list(range(3))).labels
    assert data.values == [names, salaries, cash_flow]
    assert data.get(key=1) == salaries
    assert data.get(key=2).max() == 10000


@pytest.mark.parametrize(
    "function",
    [DataFrame],
)
def test_docstrings(function):
    assert function.__doc__ is not None