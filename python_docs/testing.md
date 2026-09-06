# Testy — `pytest`

## Podstawy

```python
# plik: test_math.py

def multiply(a, b):
    return a * b

def test_multiply_positive():
    assert multiply(3, 4) == 12

def test_multiply_by_zero():
    assert multiply(5, 0) == 0

def test_multiply_negative():
    assert multiply(-2, 3) == -6
```

```bash
uv run pytest               # uruchom wszystkie testy
uv run pytest -v            # verbose — widać nazwy testów
uv run pytest -k multiply   # uruchom tylko testy z "multiply" w nazwie
```

pytest sam znajduje testy w projekcie — rozpoznaje je po nazwach. Plik musi
nazywać się `test_*.py`, funkcja testowa musi zaczynać się od `test_`, a klasa
grupująca testy od `Test` (taka klasa nie może mieć `__init__`). Nic nie
rejestrujesz ręcznie, wystarczy trzymać się tych nazw.

---

## `pytest.raises` — testowanie wyjątków

`pytest.raises` opakowuje kod, który ma rzucić wyjątek, i przekształca to w
warunek testu: test przechodzi, jeśli wyjątek poleciał, a pada, jeśli kod
wykonał się bez błędu albo rzucił wyjątek innego typu.

```python
import pytest

def test_negative_age_is_rejected():
    with pytest.raises(ValueError):
        set_age(-5)
```

Argument `match` dopasowuje wyrażenie regularne do treści komunikatu wyjątku.

```python
with pytest.raises(ValueError, match="must be positive"):
    set_age(-5)
```

---

## `@pytest.fixture` — przygotowanie danych dla testu

Fixture to funkcja, która przygotowuje obiekt potrzebny w testach, żeby nie
powtarzać tego samego kodu przygotowującego w każdym z nich. Test zgłasza
zapotrzebowanie na fixture, wpisując jej nazwę jako swój parametr. pytest
dopasowuje ten parametr po nazwie, wywołuje odpowiednią fixture i podstawia
jej wynik pod ten argument.

```python
import pytest

@pytest.fixture
def sample_users():
    return [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]


def test_count(sample_users):        # nie wywołujesz sample_users() samodzielnie
    assert len(sample_users) == 2

def test_oldest(sample_users):
    assert max(sample_users, key=lambda u: u["age"])["name"] == "Alice"
```

Każdy test dostaje własny, świeżo utworzony wynik fixture, więc testy nie
mogą sobie nawzajem popsuć danych.

### Sprzątanie po teście — `yield`

Jeżeli fixture otwiera zasób, który trzeba potem zamknąć, zamiast `return`
używasz `yield`. Kod przed `yield` przygotowuje zasób i zwraca go do testu,
a kod po `yield` wykonuje się po zakończeniu testu — również wtedy, gdy test
padł.

```python
@pytest.fixture
def db_conn():
    conn = connect()
    yield conn          # tę wartość dostaje test
    conn.close()        # to wykona się po teście
```

### Cykl życia fixture — `scope`

Domyślnie pytest wywołuje fixture osobno dla każdego testu, który jej
potrzebuje. Parametr `scope` pozwala współdzielić raz przygotowany wynik
między wieloma testami, gdy przygotowanie jest kosztowne.

```python
@pytest.fixture(scope="session")     # dostępne też: "module", "class", "function"
def http_client():
    ...
```

Przy `scope="session"` pytest utworzy fixture raz na całe uruchomienie testów,
zamiast osobno dla każdego z nich.

### Fixture wspólne dla wielu plików — `conftest.py`

Fixture zapisane w pliku `conftest.py` są widoczne dla wszystkich testów z
tego katalogu i katalogów niżej, bez potrzeby ich importowania.

---

## `@pytest.mark.parametrize` — ten sam test na wielu danych

`parametrize` pozwala opisać kilka zestawów danych wejściowych dla jednego
testu, zamiast kopiować ten sam test z różnymi wartościami. Pierwszy argument
dekoratora wymienia nazwy parametrów testu, drugi to lista krotek z
wartościami dla kolejnych przypadków.

```python
@pytest.mark.parametrize("a, b, expected", [
    (3, 4, 12),
    (5, 0, 0),
    (-2, 3, -6),
])
def test_multiply(a, b, expected):
    assert multiply(a, b) == expected
```

pytest uruchamia to jako trzy niezależne testy. Jeśli jeden z nich padnie,
pozostałe i tak się wykonają, a raport wskaże dokładnie ten zestaw danych,
który zawiódł.

---

## `unittest.mock` — mockowanie w testach

Załóżmy, że w pliku `my_module.py` masz te dwie funkcje:

```python
# plik: my_module.py

async def fetch_user(id: int) -> dict:
    # tu w środku prawdziwy request HTTP do API
    ...

async def get_username(id: int) -> str:
    user = await fetch_user(id)
    return user["name"]
```

Test na `get_username` nie powinien faktycznie wysyłać requestu przez
`fetch_user` — jest wolny, kosztowny i może dać różny wynik za każdym razem.
Dekorator `@patch` podmienia `fetch_user` na obiekt typu mock na czas jednego
testu i przywraca oryginał po jego zakończeniu.

Ten mock `@patch` przekazuje jako pierwszy dodatkowy argument dekorowanej
funkcji testowej. `mock_fetch` to po prostu nazwa, którą sami wybraliśmy dla
tego parametru, żeby było wiadomo, co reprezentuje — gdybyś nazwał go
inaczej, np. `m`, działałoby tak samo. `@patch` nie dopasowuje niczego po
nazwie, tylko po kolejności argumentów.

```python
from unittest.mock import AsyncMock, patch

@patch("my_module.fetch_user")
async def test_get_username(mock_fetch):
    mock_fetch.return_value = {"name": "Alice"}

    result = await get_username(1)

    assert result == "Alice"
    mock_fetch.assert_called_once_with(1)
```

Atrybut `return_value` ustawia, co mock ma zwrócić przy wywołaniu.
Metoda `assert_called_once_with(1)` sprawdza, że mock został wywołany
dokładnie raz i z argumentem `1` — test padnie, jeśli wywołań było więcej,
mniej, albo z innym argumentem.

`patch` domyślnie podmienia obiekt na `Mock` — obiekt, który przy wywołaniu
zwraca `return_value` niezależnie od przekazanych argumentów. Gdy podmieniana
funkcja jest zdefiniowana jako `async def`, trzeba użyć `AsyncMock` zamiast
`Mock`, bo `get_username` robi na niej `await`, a zwykły `Mock` nie jest
awaitable.

```python
@patch("my_module.fetch_user", new_callable=AsyncMock)
async def test_get_username(mock_fetch):
    mock_fetch.return_value = {"name": "Alice"}
    ...
```

<!-- nowa wiedza ląduje powyżej tej linii -->
