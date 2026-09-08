# Python Learning Notes

Tu ląduje nowa wiedza w miarę jak budujemy projekt.
Przykłady są celowo niezwiązane z projektem — chodzi o zrozumienie konceptu.

---

## Typy danych — `str`, `int`, `float`, `bool`

Python jest dynamicznie typowany — nie deklarujesz typu zmiennej.

```python
city = "Warsaw"       # str — tekst
temperature = 21.5    # float — liczba z przecinkiem
population = 1800000  # int — liczba całkowita
is_capital = True     # bool — prawda/fałsz

# rzutowanie (konwersja między typami)
temperature = float("21.5")   # ze stringa na float
text = str(1800000)           # z inta na stringa
```

---

## Instrukcje warunkowe — `if`, `elif`, `else`

```python
age = 20

if age >= 18:
    print("dorosły")
elif age >= 13:
    print("nastolatek")
else:
    print("dziecko")
```

---

## Pętle — `for`, `while`

```python
colors = ["red", "green", "blue"]

# for — kiedy wiesz po czym iterujesz
for color in colors:
    print(color)

# enumerate — kiedy potrzebujesz też indeksu
for i, color in enumerate(colors):
    print(f"{i}: {color}")

# while — kiedy nie wiesz ile razy
count = 0
while count < 3:
    print(count)
    count += 1
```

---

## Kolekcje — `list`, `dict`, `set`, `tuple`

### list — lista, kolejność ma znaczenie

```python
fruits = []
fruits.append("apple")    # dodaj na koniec
fruits.remove("apple")    # usuń element
fruits[0]                 # pierwszy element
fruits[-1]                # ostatni element
len(fruits)               # liczba elementów
```

#### Slicing — wycinanie kawałków listy

Składnia: `lista[start:stop:step]` — `stop` jest **wykluczone**.

```python
nums = [10, 20, 30, 40, 50, 60]

nums[1:3]      # [20, 30]      — od indeksu 1 do 3 (bez 3)
nums[:3]       # [10, 20, 30]  — od początku do 3
nums[3:]       # [40, 50, 60]  — od 3 do końca
nums[-2:]      # [50, 60]      — ostatnie 2
nums[::2]      # [10, 30, 50]  — co drugi
nums[::-1]     # [60, 50, ...] — odwrócona lista

# top 5 elementów (przyda się w projekcie)
top_5 = nums[:5]
```

Działa też na stringach: `"abcdef"[1:4]` → `"bcd"`.

### dict — słownik, klucz → wartość

```python
person = {
    "name": "Alice",
    "age": 30,
    "city": "Warsaw"
}

person["name"]            # "Alice"
person.get("email", "")   # "" jeśli klucz nie istnieje
person.keys()             # wszystkie klucze
person.values()           # wszystkie wartości
person.items()            # pary (klucz, wartość)
```

### set — zbiór, bez duplikatów, bez kolejności

```python
roles = {"admin", "editor", "viewer"}
"admin" in roles          # True — szybkie sprawdzanie przynależności
roles.add("moderator")

# deduplikacja listy — najczęstsze zastosowanie
unique = set([1, 1, 2, 3, 3])   # {1, 2, 3}
```

### tuple — krotka, niemutowalna

```python
point = (10, 20)          # nie możesz zmienić wartości
x, y = point              # rozpakowanie (unpacking)
```

---

## Funkcje

```python
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Alice")             # Hello, Alice!
greet("Bob", "Hi")         # Hi, Bob!

# funkcja zwraca wartość
def square(n):
    return n * n

# *args — dowolna liczba argumentów
def add_all(*numbers):
    return sum(numbers)

add_all(1, 2, 3, 4)        # 10

# **kwargs — argumenty nazwane
def describe(**info):
    for key, value in info.items():
        print(f"{key}: {value}")

describe(name="Alice", age=30)
```

---

## Klasy

Klasa to szablon. Tworzysz wiele obiektów (instancji) według tego szablonu.

```python
class Dog:
    def __init__(self, name: str, breed: str):
        self.name = name
        self.breed = breed

    def __str__(self):
        return f"{self.name} ({self.breed})"

    def __repr__(self):
        return f"Dog(name='{self.name}', breed='{self.breed}')"

    def bark(self) -> str:
        return f"{self.name} says: Woof!"


rex = Dog("Rex", "Labrador")
print(rex)          # Rex (Labrador)   ← używa __str__
rex.bark()          # Rex says: Woof!
```

Metody typu `__init__`, `__str__`, `__repr__` nazywa się **dunderami** (double underscore).

### Dziedziczenie

```python
class GuideDog(Dog):
    def __init__(self, name, breed, owner: str):
        super().__init__(name, breed)
        self.owner = owner

    def __str__(self):
        return f"{super().__str__()} — guide dog of {self.owner}"
```

### dataclass — skrócony zapis

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

---

## Wyjątki — `try`, `except`, `raise`

```python
# łapanie wyjątku
try:
    result = 10 / 0
except ZeroDivisionError:
    print("nie dziel przez zero")

# łapanie kilku typów naraz + odczytanie wyjątku
try:
    value = int(user_input)
except (ValueError, TypeError) as e:
    print(f"bad input: {e}")

# własny wyjątek — minimalna wersja
class TooYoungError(Exception):
    pass

def buy_alcohol(age: int):
    if age < 18:
        raise TooYoungError(f"Za młody: {age} lat")

# własny wyjątek — z domyślną wiadomością
class InsufficientFundsError(Exception):
    def __init__(self):
        super().__init__("Account balance is too low")

raise InsufficientFundsError()   # nie musisz podawać wiadomości przy rzucaniu
```

---

## Context manager — `with`

Gdy otwierasz zasób (plik, połączenie, lock), musisz go zamknąć — nawet jeśli po drodze poleci wyjątek.

```python
# ręcznie — brzydko i łatwo zapomnieć
f = open("data.txt")
try:
    content = f.read()
finally:
    f.close()

# z `with` — zamknięcie jest gwarantowane
with open("data.txt") as f:
    content = f.read()
# tutaj plik jest już zamknięty, nawet jeśli read() rzucił wyjątek
```

Analogia do Javy: to dokładnie `try-with-resources`. `with` w Pythonie = `try (var f = new FileReader(...))`.

### Jak to działa pod spodem

Obiekt jest context managerem, jeśli ma dwie metody dunder:

- `__enter__()` — wywoływana na wejściu, jej wynik ląduje w `as f`
- `__exit__()` — wywoływana na wyjściu, **zawsze**: po sukcesie i po wyjątku

Odpowiednik `AutoCloseable` z Javy, tylko z dwiema metodami zamiast jednej.

```python
class Timer:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print(f"took {time.time() - self.start:.2f}s")

with Timer():
    do_something()
```

### Kilka zasobów naraz

```python
with open("in.txt") as src, open("out.txt", "w") as dst:
    dst.write(src.read())
```

### `async with` — wersja asynchroniczna

Gdy otwarcie lub zamknięcie zasobu samo wymaga czekania (np. nawiązanie połączenia sieciowego), context manager musi być async. Wtedy zamiast `__enter__`/`__exit__` ma `__aenter__`/`__aexit__`, a używasz go przez `async with`:

```python
async with open_connection() as conn:      # tylko wewnątrz `async def`
    await conn.send("ping")
# połączenie zamknięte asynchronicznie
```

Reguła jest ta sama co przy `await` — `async with` działa wyłącznie w funkcji `async def`.

---

## List comprehensions

Skrócony zapis pętli `for`, która buduje nową listę.

```python
numbers = [1, 2, 3, 4, 5, 6]

# zamiast:
evens = []
for n in numbers:
    if n % 2 == 0:
        evens.append(n)

# piszesz:
evens = [n for n in numbers if n % 2 == 0]   # [2, 4, 6]

squares = [n * n for n in numbers]            # [1, 4, 9, 16, 25, 36]
```

---

## Wbudowane funkcje — `sorted`, `sum`, `any`, `all`, `filter`, `map`

```python
nums = [3, 1, 4, 1, 5, 9]

sum(nums)                        # 23
max(nums)                        # 9
min(nums)                        # 1
sorted(nums)                     # [1, 1, 3, 4, 5, 9]
sorted(nums, reverse=True)       # [9, 5, 4, 3, 1, 1]

any(n > 8 for n in nums)        # True — czy któryś > 8?
all(n > 0 for n in nums)        # True — czy wszystkie > 0?
```

### `sorted` z `key=` — sortowanie po atrybucie

Gdy sortujesz obiekty (a nie liczby), musisz powiedzieć "po czym sortuj":

```python
users = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35},
]

# key= dostaje funkcję która z elementu wyciąga wartość do sortowania
sorted(users, key=lambda u: u["age"])
# [Bob (25), Alice (30), Charlie (35)]

sorted(users, key=lambda u: u["age"], reverse=True)
# malejąco
```

### `lambda` — anonimowa funkcja jednolinijkowa

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

## Moduł `collections`

```python
from collections import defaultdict, Counter

# Counter — zlicz elementy
words = ["apple", "banana", "apple", "cherry", "apple"]
c = Counter(words)
# Counter({'apple': 3, 'banana': 1, 'cherry': 1})
c.most_common(2)                 # [('apple', 3), ('banana', 1)]

# defaultdict — dict z domyślną wartością dla nowych kluczy
scores = defaultdict(int)
scores["Alice"] += 10            # nie musisz inicjalizować klucza
scores["Bob"] += 5
```

---

## Type hints

Python nie wymusza typów, ale możesz je opisać. IDE dzięki temu podpowiada i wyłapuje błędy.

```python
def greet(name: str, times: int) -> str:
    return (name + " ") * times

def first(items: list[int]) -> int | None:
    return items[0] if items else None
```

### `X | None` i `Optional[X]` — wartość może być None

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

### `Any` — wyłącz typowanie

Gdy nie wiesz co tam będzie (np. surowe dane z API zanim je sparsujesz):

```python
from typing import Any

def parse_response(data: dict[str, Any]) -> User:
    # data może mieć dowolne wartości pod kluczami
    ...
```

`Any` mówi type checkerowi: "zostaw mnie w spokoju, nie sprawdzaj".

---

## f-strings i formatowanie tekstu

```python
name = "Alice"
score = 9.5

print(f"Player: {name}, score: {score:.1f}")   # Player: Alice, score: 9.5
print(f"{score:>10.2f}")                        # "      9.50" — wyrównaj do prawej
print(f"{name:<10} {score:>6.2f}")             # "Alice          9.50"
```

---

## Importy i moduły

```python
# import z biblioteki standardowej
from datetime import datetime
from collections import Counter

# import z własnego pliku (np. dog.py)
from dog import Dog

# sprawdzenie bieżącego czasu
now = datetime.now()
print(now.strftime("%Y-%m-%d %H:%M"))
```

---

## `if __name__ == "__main__"`

```python
# ten blok uruchamia się tylko gdy piszesz: python script.py
# NIE uruchamia się gdy ktoś robi: from script import something

def main():
    print("start")

if __name__ == "__main__":
    main()
```

---

## Enum

Enum to zbiór nazwanych stałych. Zamiast trzymać magiczne stringi czy inta — masz typ.

```python
from enum import Enum

class Direction(Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"

d = Direction.NORTH
d.name     # "NORTH"
d.value    # "north"

d == Direction.NORTH   # True
```

Możesz iterować po wszystkich wartościach:

```python
for direction in Direction:
    print(direction.name, direction.value)
```

## `__init__.py` — po co ten plik?

Pusty plik `__init__.py` w katalogu mówi Pythonowi: "ten katalog to paczka (package)".

Bez niego Python nie pozwoli robić importów z tego katalogu:

```python
from expense_tracker.expense import Expense  # działa — bo jest __init__.py
```

To jak `package` w Javie — bez deklaracji paczki klasa jest "bezdomna".

Plik może być pusty albo zawierać kod inicjalizacyjny paczki (np. re-eksporty).

## `*args` — dowolna liczba argumentów

```python
def print_all(*names: str):
    for name in names:
        print(name)

print_all("Alice", "Bob", "Charlie")
```

Wewnątrz funkcji `names` to tuple.

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

<!-- nowa wiedza ląduje powyżej tej linii -->
