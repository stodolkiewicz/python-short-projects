# Python Learning Notes

Tu ląduje nowa wiedza w miarę jak budujemy projekt.
Przykłady są celowo niezwiązane z projektem — chodzi o zrozumienie konceptu.

---

## uv — menedżer pakietów i środowisk

`uv` to nowoczesny zamiennik `pip` + `venv`. Szybszy, prostszy.

```bash
# uruchom skrypt
uv run main.py

# dodaj zależność do projektu (zapisuje w pyproject.toml)
uv add requests

# usuń zależność
uv remove requests

# zainstaluj wszystkie zależności z pyproject.toml
uv sync

# uruchom testy
uv run pytest

# sprawdź jakie paczki są zainstalowane
uv pip list
```

Plik `pyproject.toml` to serce projektu — tam są zależności i konfiguracja.
Plik `uv.lock` to "zamrożone" wersje — nie edytuj go ręcznie.

---

## Uruchamianie projektu

```bash
uv run main.py
```

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
```

---

## Wyjątki — `try`, `except`, `raise`

```python
# łapanie wyjątku
try:
    result = 10 / 0
except ZeroDivisionError:
    print("nie dziel przez zero")

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

## Testy — `pytest`

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
uv run pytest        # uruchom wszystkie testy
uv run pytest -v     # verbose — widać nazwy testów
```

Asercja to stwierdzenie "to musi być prawdą". Jeśli nie jest — test pada.

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
from expense_tracker.Expense import Expense   # działa — bo jest __init__.py
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

<!-- nowa wiedza ląduje powyżej tej linii -->
