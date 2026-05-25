# Projekt 2 — Crypto Analyzer

Nowe rzeczy z Pythona poznane podczas budowy Crypto Analyzera.

---

## `@dataclass` — skrócony zapis klasy

Python generuje `__init__`, `__repr__` i `__eq__` automatycznie na podstawie zadeklarowanych pól.

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

p = Point(1.0, 2.5)
# Python sam generuje __init__, __repr__, __eq__

# wartości domyślne
@dataclass
class User:
    name: str
    age: int = 18
```

Analogia do Javy: jak Lombok `@Data` — generuje boilerplate za Ciebie.

### `@classmethod` — statyczna fabryka

```python
@dataclass
class Coin:
    id: str
    name: str

    @classmethod
    def from_dict(cls, data: dict) -> "Coin":
        return cls(id=data["id"], name=data["name"])
```

- `@classmethod` — metoda należy do klasy, nie do instancji
- `cls` — wskazuje na klasę (jak `self` na instancję); `cls(...)` tworzy nową instancję
- `-> "Coin"` — cudzysłowy bo klasa jest jeszcze definiowana w tym miejscu; bez nich błąd
- Analogia do Javy: statyczna metoda fabryczna `Coin.fromDict(data)`

---

## `datetime` — praca z datami

```python
from datetime import datetime

# parsowanie stringa z API (format ISO 8601)
dt = datetime.fromisoformat("2024-01-15T12:30:00+00:00")

dt.year        # 2024
dt.month       # 1
dt.day         # 15

# formatowanie do stringa
dt.strftime("%Y-%m-%d %H:%M")   # "2024-01-15 12:30"
```

---

## `X | None` i `Optional[X]` — wartość może być None

Gdy funkcja czasami zwraca `None` (np. "nie znalazłem"), musisz to powiedzieć w type hincie:

```python
def find_user(id: int) -> str | None:
    if user_exists(id):
        return "Alice"
    return None                  # bez `| None` type checker krzyczy
```

`Optional[str]` to **dokładnie to samo** co `str | None`. Dwie składnie:
- `Optional[str]` — stara (Python 3.5+), wymaga `from typing import Optional`
- `str | None` — nowa (Python 3.10+), bez importu, preferowana

```python
from typing import Optional

def find_user(id: int) -> Optional[str]:   # to samo co `str | None`
    ...
```

---

## `Any` — wyłącz typowanie

Gdy nie wiesz co tam będzie (np. surowe dane z API zanim je sparsujesz):

```python
from typing import Any

def parse_response(data: dict[str, Any]) -> User:
    # data może mieć dowolne wartości pod kluczami
    ...
```

`Any` mówi type checkerowi: "zostaw mnie w spokoju, nie sprawdzaj".

---

## `async` / `await` — programowanie asynchroniczne

Async to sposób na robienie kilku rzeczy "naraz" w jednym wątku — zwłaszcza takich, które **czekają** (np. odpowiedź z API, odczyt pliku).

Analogia: piekarz wstawia chleb do pieca i zamiast stać 30 minut, w tym czasie zarabia ciasto na pizzę. Async to ten piekarz.

```python
import asyncio

# funkcja async — definiowana z `async def`
async def fetch_user(id: int) -> str:
    print(f"pobieram użytkownika {id}...")
    await asyncio.sleep(1)              # symulujemy czekanie na API
    return f"user_{id}"

# uruchamianie funkcji async — przez asyncio.run()
async def main():
    user = await fetch_user(1)          # czekaj na wynik
    print(user)

asyncio.run(main())                     # punkt wejścia
```

### Kluczowe pojęcia

- `async def` — definiuje **korutynę** (coroutine), nie zwykłą funkcję
- `await` — "poczekaj na wynik tej korutyny, w tym czasie inne mogą działać"
- `await` można wywołać **tylko wewnątrz `async def`**
- `asyncio.run(...)` — uruchamia całość, jeden raz, na samej górze programu

### Równoległe wywołania — `asyncio.gather`

Tu się dzieje magia. `gather` startuje wszystkie korutyny "naraz":

```python
async def main():
    # po kolei — 3 sekundy
    a = await fetch_user(1)
    b = await fetch_user(2)
    c = await fetch_user(3)

    # równolegle — 1 sekunda
    a, b, c = await asyncio.gather(
        fetch_user(1),
        fetch_user(2),
        fetch_user(3),
    )
```

### `async for` — iteracja po asynchronicznym źródle

Gdy źródło danych samo jest async (np. strumień zdarzeń):

```python
async for event in event_stream():
    print(event)
```

---

## Context managers — `with`

Obiekt który implementuje `__enter__` i `__exit__` — Python wywołuje je automatycznie na wejściu i wyjściu z bloku `with`. Gwarantuje sprzątanie nawet gdy poleci wyjątek.

```python
with open("file.txt") as f:
    data = f.read()
# plik zamknięty automatycznie — nawet przy wyjątku
```

Analogia do Javy: `try-with-resources`.

Wersja async używa `__aenter__` / `__aexit__` i `async with`:

```python
async with httpx.AsyncClient() as client:
    response = await client.get(url)
# klient zamknięty automatycznie
```

---

## `httpx` — HTTP client (sync i async)

Biblioteka do wysyłania requestów HTTP. Działa tak samo sync i async — wybierasz przez wybór klienta.

```bash
uv add httpx
```

```python
import httpx
import asyncio

# wersja async
async def get_user(id: int) -> dict:
    async with httpx.AsyncClient() as client:        # `async with` zamiast `with`
        response = await client.get(f"https://api.example.com/users/{id}")
        response.raise_for_status()                  # rzuca wyjątek przy 4xx/5xx
        return response.json()                       # parsuje JSON do dict

asyncio.run(get_user(1))
```

### Co się tu dzieje

- `httpx.AsyncClient()` — klient z connection pool (jak `RestTemplate` w Spring)
- `async with` — context manager dla async (otwiera i zamyka klienta automatycznie)
- `await client.get(...)` — wysyła request, czeka na odpowiedź
- `.json()` — gotowy parser, zwraca `dict` albo `list`
- `.raise_for_status()` — automatyczna walidacja kodu HTTP

### Łapanie błędów

```python
try:
    response = await client.get(url)
    response.raise_for_status()
except httpx.HTTPError as e:
    print(f"błąd HTTP: {e}")
```

---

## Wyjątki — łapanie kilku typów

```python
# łapanie kilku typów naraz + odczytanie wyjątku
try:
    value = int(user_input)
except (ValueError, TypeError) as e:
    print(f"bad input: {e}")
```

---

## `lambda` — anonimowa funkcja jednolinijkowa

```python
# zamiast:
def get_age(user):
    return user["age"]

# piszesz:
lambda user: user["age"]
```

Składnia: `lambda argumenty: wyrażenie`. Brak `return` — wynik wyrażenia jest zwracany automatycznie. Używana głównie tam, gdzie funkcja jest mała i jednorazowa — np. jako `key=` w `sorted`.

Analogia do Javy: dokładnie to samo co `user -> user.getAge()`.

---

## `sorted` z `key=` — sortowanie po atrybucie

Gdy sortujesz obiekty (a nie liczby), musisz powiedzieć "po czym sortuj":

```python
users = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35},
]

sorted(users, key=lambda u: u["age"])
# [Bob (25), Alice (30), Charlie (35)]

sorted(users, key=lambda u: u["age"], reverse=True)
# malejąco
```

---

## Slicing — wycinanie kawałków listy

Składnia: `lista[start:stop:step]` — `stop` jest **wykluczone**.

```python
nums = [10, 20, 30, 40, 50, 60]

nums[1:3]      # [20, 30]      — od indeksu 1 do 3 (bez 3)
nums[:3]       # [10, 20, 30]  — od początku do 3
nums[3:]       # [40, 50, 60]  — od 3 do końca
nums[-2:]      # [50, 60]      — ostatnie 2
nums[::2]      # [10, 30, 50]  — co drugi
nums[::-1]     # [60, 50, ...] — odwrócona lista

# top 5 elementów
top_5 = nums[:5]
```

Działa też na stringach: `"abcdef"[1:4]` → `"bcd"`.

---

## `Counter` — zliczanie kategorii

```python
from collections import Counter

words = ["apple", "banana", "apple", "cherry", "apple"]
c = Counter(words)
# Counter({'apple': 3, 'banana': 1, 'cherry': 1})

c["apple"]           # 3
c.most_common(2)     # [('apple', 3), ('banana', 1)]
```

Możesz też inkrementować ręcznie — `Counter` dziedziczy po `dict`, więc `c["klucz"]` działa jak słownik. Nowy klucz startuje automatycznie od `0` (jak `defaultdict(int)`):

```python
c = Counter()
c["above"] += 1   # c["above"] nie istniało → zaczyna od 0, po += 1 wynosi 1
c["below"] += 1
c["above"] += 1
# Counter({'above': 2, 'below': 1})
```

---

## `unittest.mock` — mockowanie w testach

Gdy nie chcesz, żeby test naprawdę dzwonił do API (wolne, kosztowne, niedeterministyczne) — podmieniasz funkcję na fejk.

```python
from unittest.mock import AsyncMock, patch

@patch("my_module.fetch_user")               # podmień fetch_user w my_module
async def test_get_username(mock_fetch):
    mock_fetch.return_value = {"name": "Alice"}    # co fejk zwróci

    result = await get_username(1)

    assert result == "Alice"
    mock_fetch.assert_called_once_with(1)    # czy zostało wywołane jak trzeba
```

- `Mock` — dla zwykłych funkcji
- `AsyncMock` — dla `async def` funkcji (zwracają to co `return_value`, ale są awaitable)
- `@patch("path.to.thing")` — podmienia obiekt na czas testu
- `mock.return_value` — co fejk ma zwrócić
- `mock.assert_called_once_with(...)` — weryfikuje że było wywołane
