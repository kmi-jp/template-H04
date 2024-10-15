# H04: Data 1

Vytvořte balíček `data`, který obsahuje moduly `exceptions.py`, `indexed_container.py`, `index.py`, `series.py` a `dataframe.py`. U tříd a metod **nezapomínejte na docstringy**.

---

## Soubor `exceptions.py`

Modul `exceptions.py` obsahuje definice tří výjimek `InvalidDataError`, `IndexMismatchError` a `DuplicateKeyError`:

* `InvalidDataError` a `IndexMismatchError` dědí od `Exception` a nepřidávají žádnou další funkcionalitu.
* `DuplicateKeyError` dědí od `Exception` a navíc v atributu `DuplicateKeyError.dupliactes` uchovává seznam duplicitních klíčů.

```python
from data.exceptions import DuplicateKeyError


try:
    raise DuplicateKeyError([1, 2, 3, 2, 1])
except DuplicateKeyError as err:
    assert 1 in err.duplicates
    assert 2 in err.duplicates
    assert len(err.duplicates) == 2
```

---

## Třída `Index`

Modul `index.py` obsahuje třídu `Index` sloužící k indexaci libovolné sekvence hodnot.

```python
from data.index import Index


idx = Index(["key 1", "key 2", "key 3", "key 4", "key 5"])
values = [0, 1, 2, 3, 4]

assert values[idx.get_loc("key 2")] == 1
```

Třída obsahuje následující vlastnosti:

* `Index.labels` - seznam klíču (labelů) - nesmí obsahovat duplicity (vyvolá výjimku `DuplicateKeyError`) a musí mít alespoň jeden prvek (jinak vyvolá výjimku `InvalidDataError`).
* `Index.name` - volitelná vlastnost obsahující název indexu, výchozí hodnota na `""`.

Třída obsahuje následující metody:

* `Index.get_loc(self, key)` - přeloží klíč `key` z `Index.labels` na odpovídající index. Pokud není klíč přítomen vyvoláme výjimku `KeyError`.

```python
from data.index import Index


idx = Index(["user 1", "user 2", "user 3", "user 4", "user 5"])

assert idx.name == ""
assert idx.labels == ["user 1", "user 2", "user 3", "user 4", "user 5"]

idx = Index(["user 1", "user 2", "user 3", "user 4", "user 5"], name="users")

assert idx.name == "users"
assert idx.labels == ["user 1", "user 2", "user 3", "user 4", "user 5"]
```

```python
idx = Index(["user 1", "user 2", "user 3", "user 4", "user 5"])

assert idx.get_loc("user 2") == 1
```

---

## Třída `IndexedContainer`

Modul `indexed_container.py` obsahuje třídu `IndexedContainer` reprezentující datovou strukturu, jejíž hodnoty jsou indexované objektem třídy `Index`.

Třída obsahuje následující vlastnosti:

* `IndexedContainer.values` - seznam hodnot uložený v kontejneru, musí obsahovat alespoň jeden prvek jinak vyvolá `InvalidDataError`.
* `IndexedContainer.index` - index sloužící k indexaci `IndexedContainer.values`, musí být stejné délky jako `IndexedContainer.values` jinak vyvolá `IndexMismatchError`. Pokud byla počáteční hodnota `None` vytvoříme index nový, `Index.labels` nastavíme na hodnoty `0` až `n - 1` kde `n` je délka `IndexedContainer.values`.

Třída obsahuje následující metody:

* `IndexedContainer.get(self, key)` - pokud `IndexedContainer.index` obsahuje `key`, vrátí odpovídající hodnotu z `IndexedContainer.values`, jinak vrací `None`.

```python
from data.indexed_container import IndexedContainer


# index
users = Index(["user 1", "user 2", "user 3", "user 4"], name="names")

# IndexedContainer indexovaný dle indexu users
numbers = IndexedContainer([1, 2, 3, 4], index=users)

assert numbers.values == [1, 2, 3, 4]
assert numbers.index.labels == ['user 1', 'user 2', 'user 3', 'user 4']

# IndexedContainer indexovaný dle výchozího indexu
numbers = IndexedContainer([1, 2, 3, 4])

assert numbers.values == [1, 2, 3, 4]
assert numbers.index.labels == [0, 1, 2, 3]
```

---

## Třída `Series`

Modul `series.py` obsahuje třídu `Series`, která dědí od `IndexedContainer`. Tato třída uchovává posloupnost hodnot indexovaných dle objektu třídy `Index`.

![Series](series.png)

```python
from data.series import Series
from data.index import Index

# index
users = Index(["user 1", "user 2", "user 3", "user 4"], name="names")

# series indexovaná dle indexu users
salaries = Series([20000, 300000, 20000, 50000], index=users)

assert salaries.values == [20000, 300000, 20000, 50000]
assert salaries.index.labels == ['user 1', 'user 2', 'user 3', 'user 4']
```

Třída dále obsahuje pouze zděděné vlastnosti `values` (hodnoty posloupnosti) a `index`.

Třída obsahuje následující metody:

* `Series.sum(self)` - sečte všechny hodnoty v posloupnosti
* `Series.max(self)` - nalezne maximální hodnotu z posloupnosti
* `Series.min(self)` - nalezne minimální hodnotu z posloupnosti, analogicky k max variantě
* `Series.mean(self)` - vypočítá aritmetický průměr
* `Series.apply(self, func)` - aplikuje libovolnou funkci na prvky posloupnosti
* `Series.abs(self)` - vytvoří novou Series, kde všechny hodnotu budou výsledky aplikace funkce `abs()`

Nemusíte ošetřovat datový typ hodnot v posloupnosti.

```python
from data.series import Series
from data.index import Index


users = Index(["user 1", "user 2", "user 3", "user 4"], name="names")

names = Series(["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil"], index=users)
cash_flow = Series([-100, 10000, -2000, 1100], index=users)
salaries = Series([20000, 300000, 20000, 50000], index=users)

assert salaries.values == [20000, 300000, 20000, 50000]
assert salaries.index.labels == ['user 1', 'user 2', 'user 3', 'user 4']

# situace kdy nebude předán index
no_index = Series(["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil"])
assert no_index.index.labels == [0, 1, 2, 3]

assert cash_flow.get("user 1") == -100
assert cash_flow.get("user 1000") is None

# test metod min a max
assert cash_flow.max() == 10000
assert cash_flow.min() == -2000

# test metody sum
assert cash_flow.sum() == 9000

# test metody mean
assert cash_flow.mean() == 2250.0

# test metody apply
def squared(a):
    """Returns squared number"""
    return a ** 2

result = cash_flow.apply(squared)

assert cash_flow != result
assert result.values == [10000, 100000000, 4000000, 1210000]

# test metody abs
result = cash_flow.abs()

assert cash_flow != result
assert result.values == [100, 10000, 2000, 1100]
```


<!--
```python
from data.series import Series
from data.index import Index


users = Index(["user 1", "user 2", "user 3", "user 4"], name="names")

names = Series(["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil"], index=users)
cash_flow = Series([-100, 10000, -2000, 1100], index=users)
salaries = Series([20000, 300000, 20000, 50000], index=users)

assert salaries.values == [20000, 300000, 20000, 50000]
assert salaries.index.labels == ['user 1', 'user 2', 'user 3', 'user 4']

# situace kdy nebude předán index
no_index = Series(["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil"])
assert no_index.index.labels == [0, 1, 2, 3]
```

```python
from data.series import Series
from data.index import Index


users = Index(["user 1", "user 2", "user 3", "user 4"], name="names")

cash_flow = Series([-100, 10000, -2000, 1100], index=users)

assert cash_flow.get("user 1") == -100
assert cash_flow.get("user 1000") is None
```

Dále bude možné provádět jednoduché operace na datech uložených v `Series`. Konkrétně:

### Metoda `Series.max(self)`/`Series.min(self)`

Maximální hodnota v `Series`. Nemusíte ošetřovat datový typ hodnot v posloupnosti.

```python
from data.series import Series
from data.index import Index


users = Index(["user 1", "user 2", "user 3", "user 4"], name="names")
cash_flow = Series([-100, 10000, -2000, 1100], index=users)

assert cash_flow.max() == 10000
assert cash_flow.min() == -2000
```

### Metoda `Series.sum(self)`

Součet hodnot v `Series`. Nemusíte ošetřovat datový typ hodnot v posloupnosti.

```python
from data.series import Series
from data.index import Index


users = Index(["user 1", "user 2", "user 3", "user 4"], name="names")
cash_flow = Series([-100, 10000, -2000, 1100], index=users)

assert cash_flow.sum() == 9000
```

### Metoda `Series.mean(self)`

Aritmetický průměr hodnot v `Series`. Nemusíte ošetřovat datový typ hodnot v posloupnosti. Můžete použít modul `statistics` a funkci `mean()`.

```python
from data.series import Series
from data.index import Index


users = Index(["user 1", "user 2", "user 3", "user 4", "user 5"], name="names")
cash_flow = Series([-100, 10000, -2000, 1100, 100], index=users)

assert cash_flow.mean() == 1820.0
```

### Metoda `Series.apply(self, func)`

Která aplikuje funkci `func` na všechny prvky `Series` a vrátí `Series` novou (s vypočítanými hodnotami). Původní `Series` nemodifikuje!

```python
from data.series import Series
from data.index import Index


def squared(a):
    """Returns squared number"""
    return a ** 2


users = Index(["user 1", "user 2", "user 3", "user 4"], name="names")
cash_flow = Series([-100, 10000, -2000, 1100], index=users)

result = cash_flow.apply(squared)

assert cash_flow != result
assert result.values == [10000, 100000000, 4000000, 1210000]
```

### Metoda `Series.abs(self)`

Která aplikuje funkci `abs` na všechny prvky `Series` a vrátí `Series` novou. Původní `Series` nemodifikuje! Nemusíte ošetřovat datový typ hodnot v posloupnosti.

```python
from data.series import Series
from data.index import Index


users = Index(["user 1", "user 2", "user 3", "user 4"], name="names")
cash_flow = Series([-100, 10000, -2000, 1100], index=users)

result = cash_flow.abs()

assert cash_flow != result
assert result.values == [100, 10000, 2000, 1100]
```
-->
---

## Třída `DataFrame`

Modul `dataframe.py` obsahuje třídu `DataFrame`, která slouží k reprezentaci tabulky dat. Tabulka je složena ze sloupců (alespoň jeden sloupec, každý sloupec je tvořen instancí třídy `Series`). Sloupce jsou indexovány pomoci instance třídy `Index`.

![DataFrame](dataframe.png)

Třída obsahuje pouze zděděné vlastnosti `values`(sloupce tabulky - seznam instancí třídy Series) a `index`:

* `DataFrame.values` - pokud seznam obsahuje jiný objekt než `Series`, pak skončí výjimkou  `InvalidDataError`.

```python
from data.series import Series
from data.index import Index
from data.dataframe import DataFrame


users = Index(["user 1", "user 2", "user 3", "user 4"], name="names")

salaries = Series([20000, 300000, 20000, 50000], index=users)
names = Series(["Lukas Novak", "Petr Pavel", "Pavel Petr", "Ludek Skocil"], index=users)
cash_flow = Series([-100, 10000, -2000, 1100], index=users)

data = DataFrame([names, salaries, cash_flow], index=Index(["names", "salary", "cash flow"]))

assert data.get("salary") == salaries
assert data.get("cash flow").max() == 10000
```

## Lokální testování

Funkčnost řešení ověříte následujícím příkazem:

```bash
pytest
```
