# Projekt 3 — Task Manager CLI

Menedżer zadań w terminalu. Program czyta linie wpisywane przez użytkownika
w pętli i obsługuje komendy:

- `add <treść>` — dodaje nowe zadanie o podanej treści, na start nieukończone
- `list` — wypisuje wszystkie zadania z numerem i statusem (zrobione / do zrobienia)
- `done <numer>` — oznacza zadanie o danym numerze jako ukończone
- `remove <numer>` — usuwa zadanie o danym numerze z listy
- `help` — wypisuje dostępne komendy razem z ich opisem
- `exit` — kończy program

Zadania zapisywane są do pliku `task_manager/local_db/tasks.json`, więc lista
przetrwa między uruchomieniami programu — po ponownym odpaleniu programu
widzisz te same zadania, które dodałeś poprzednio.

Komendy trzymane są w słowniku, który mapuje nazwę komendy na funkcję —
program wywołuje funkcję znalezioną w tym słowniku, zamiast rozstrzygać
komendę łańcuchem `if/elif`.

## Struktura plików

Jak w `expense_tracker/` i `crypto_analyzer/` — osobny plik na osobną
odpowiedzialność, `main.py` w korzeniu jako punkt wejścia.

- `task_manager/task.py` — klasa `Task`.
- `task_manager/storage.py` — `load_tasks` i `save_tasks`, dane trzymane w `task_manager/local_db/tasks.json`.
- `task_manager/commands.py` — funkcje komend i rejestr komend.
- `task_manager/cli.py` — `parse_command` i pętla `run()`.
- `task_manager/__init__.py` — pusty.
- `main.py` — `project3()` woła tylko `cli.run()`.

## Plan

1. `Task` (`task_manager/task.py`) — `@dataclass` z polami `id: int`, `description: str`, `done: bool = False`. Reprezentuje jedno zadanie.
2. `load_tasks() -> list[Task]` (`task_manager/storage.py`) — czyta `task_manager/local_db/tasks.json` i zwraca listę zadań. Jeśli plik nie istnieje, zwraca pustą listę zamiast rzucać wyjątek.
3. `save_tasks(tasks: list[Task]) -> None` (`task_manager/storage.py`) — zapisuje listę zadań do `task_manager/local_db/tasks.json`.
4. `parse_command(line: str) -> tuple[str, str]` (`task_manager/cli.py`) — rozdziela wpisaną linię na nazwę komendy i resztę argumentów, np. `"add Kup mleko"` → `("add", "Kup mleko")`.
5. Funkcje komend (`task_manager/commands.py`). Każda ma przyjmować te same dwa argumenty, `tasks: list[Task]` i `arg: str`, i nic nie zwracać (`def nazwa(tasks: list[Task], arg: str) -> None:`):
   - `add_task` — dopisuje nowe `Task` do listy.
   - `list_tasks` — wypisuje zadania z numerem i statusem.
   - `done_task` — ustawia `done = True` dla zadania o podanym numerze.
   - `remove_task` — usuwa zadanie o podanym numerze z listy.
   - `help_command` — wypisuje dostępne komendy.
6. Rejestr komend (`task_manager/commands.py`) — słownik `{"add": add_task, "list": list_tasks, ...}` mapujący nazwę komendy na odpowiednią funkcję z punktu 5.
7. `run()` (`task_manager/cli.py`) — wczytuje zadania przez `load_tasks`, uruchamia pętlę `while`, w każdym obiegu: czyta linię, parsuje ją przez `parse_command`, szuka komendy w rejestrze i wywołuje znalezioną funkcję. Nieznana komenda wypisuje komunikat błędu zamiast wywalać program. Komenda `exit` przerywa pętlę i wywołuje `save_tasks` na końcu.

Nowe rzeczy z Pythona, które poznamy podczas budowy Task Managera.

---

## `try/except/else/finally`

Blok `else` wykonuje się tylko wtedy, gdy kod w `try` nie rzucił wyjątku.
Blok `finally` wykonuje się zawsze — niezależnie od tego, czy wyjątek poleciał
czy nie.

```python
try:
    value = int(input("Podaj liczbę: "))
except ValueError:
    print("To nie jest liczba")
else:
    print(f"Wpisałeś {value}")
finally:
    print("Koniec próby")
```

---

## Docstringi

Docstring to string w potrójnym cudzysłowie umieszczony bezpośrednio pod
definicją funkcji — Python zapisuje go w atrybucie `__doc__` tej funkcji,
więc można go odczytać w trakcie działania programu, nie tylko przeczytać
w kodzie.

```python
def add(a: int, b: int) -> int:
    """Return the sum of a and b."""
    return a + b

print(add.__doc__)   # "Return the sum of a and b."
```

---

## Funkcje jako wartości

Funkcję można przypisać do zmiennej albo umieścić w słowniku, tak jak
dowolną inną wartość — bez wywoływania jej nawiasami. Wywołanie następuje
dopiero wtedy, gdy dodasz `()` do wyniku wyszukania w słowniku.

```python
def greet():
    print("hello")

def bye():
    print("bye")

commands = {"greet": greet, "bye": bye}
commands["greet"]()   # hello
```

---

## `json` — zapis i odczyt danych

```python
import json

data = {"name": "Alice", "age": 30}

text = json.dumps(data)      # dict -> string JSON
back = json.loads(text)      # string JSON -> dict

with open("data.json", "w") as f:
    json.dump(data, f)       # zapis od razu do pliku

with open("data.json") as f:
    data = json.load(f)      # odczyt od razu z pliku
```

`dumps`/`loads` operują na stringu, `dump`/`load` operują na pliku otwartym
przez `with`.

---

## `dataclasses.asdict` — obiekt z powrotem na `dict`

`json.dump` umie zapisać tylko podstawowe typy (`dict`, `list`, `str`, `int`,
`bool`, `None`) — obiekt `@dataclass` nie jest żadnym z nich, więc trzeba go
najpierw zamienić na `dict`. `asdict` robi dokładnie to, automatycznie, na
podstawie pól zadeklarowanych w klasie.

```python
from dataclasses import dataclass, asdict

@dataclass
class Point:
    x: float
    y: float

p = Point(1.0, 2.5)
asdict(p)   # {"x": 1.0, "y": 2.5}
```

Przy liście obiektów robisz to dla każdego elementu, np. przez list
comprehension: `[asdict(p) for p in points]`.

---

## Walrus operator `:=`

Przypisuje wartość do zmiennej i jednocześnie zwraca tę wartość jako wynik
wyrażenia — dzięki temu przypisanie może stać się częścią warunku pętli albo
`if`, bez osobnej linijki na samo przypisanie.

```python
while (line := input("> ")) != "exit":
    print(line)
```

Bez `:=` trzeba by przypisać `line` przed pętlą i jeszcze raz na jej końcu,
żeby warunek widział nową wartość przy każdym obiegu.

---

## `is` vs `==`

`==` porównuje wartości. `is` sprawdza tożsamość — czy to dokładnie ten sam
obiekt w pamięci. `None` jest w Pythonie singletonem (istnieje tylko jedna
jego instancja), więc porównania z `None` zawsze robi się przez `is`.

```python
x = None

if x is None:
    print("brak wartości")
```

---

## Truthiness

Pusta lista, pusty string, `0` i `None` są w warunku traktowane jak `False` —
nie trzeba ich porównywać do długości ani do konkretnej wartości.

```python
items = []

if items:
    print("są zadania")
else:
    print("lista pusta")
```

---

## Ternary — `x if warunek else y`

Jedno wyrażenie zamiast bloku `if/else`, gdy wynik to po prostu jedna z dwóch
wartości.

```python
status = "zrobione" if task.done else "do zrobienia"
```

---

## Unpacking z `*rest`

Gwiazdka przed nazwą zmiennej zbiera do listy wszystko, co zostało po
przypisaniu pozostałych zmiennych.

```python
first, *rest = [1, 2, 3, 4]
# first = 1
# rest = [2, 3, 4]
```

---

## `*` i `**` przy wywołaniu funkcji — rozpakowanie argumentów

To inne użycie gwiazdki niż `*rest` powyżej — tam gwiazdka zbierała wartości
przy przypisaniu, tutaj rozpakowuje je przy wywołaniu funkcji.

Pojedyncza gwiazdka `*` przed listą rozkłada jej elementy na kolejne
argumenty pozycyjne funkcji, po jednym na miejsce:

```python
def add(a, b, c):
    return a + b + c

nums = [1, 2, 3]
add(*nums)
# to samo co: add(1, 2, 3)
```

Podwójna gwiazdka `**` przed słownikiem robi to samo dla argumentów
nazwanych — każdy klucz słownika staje się nazwą argumentu, a jego wartość —
wartością tego argumentu. Działa tylko wtedy, gdy klucze słownika dokładnie
odpowiadają nazwom parametrów funkcji:

```python
d = {"id": 1, "description": "Kup mleko", "done": False}

Task(**d)
# to samo co: Task(id=1, description="Kup mleko", done=False)
```

---

## Generator expression i `next()`

`(x for x in iterable if warunek)` wygląda jak list comprehension, ale z
okrągłymi nawiasami zamiast kwadratowych — różnica jest w tym, że nie buduje
od razu całej listy w pamięci. Zamiast tego zwraca **generator**, obiekt,
który produkuje kolejne pasujące elementy jeden po drugim, na żądanie tego,
co go konsumuje.

`next(generator, default)` pobiera z generatora pierwszy element. Jeśli
generator jest pusty (nic nie pasowało do warunku), zwraca `default` zamiast
rzucać wyjątek.

```python
numbers = [1, 3, 4, 7, 8]

first_even = next((n for n in numbers if n % 2 == 0), None)
# 4 — pierwsza parzysta liczba

first_negative = next((n for n in numbers if n < 0), None)
# None — żadna nie pasuje, generator był pusty
```

To wygodny sposób na "znajdź pierwszy element spełniający warunek, albo nic"
— bez pisania osobnej pętli `for` z `break`.

---

## Metody stringów

```python
"  Kup mleko  ".strip()          # "Kup mleko" — usuwa białe znaki z brzegów
"add Kup mleko".split(" ", 1)    # ["add", "Kup mleko"] — dzieli tylko przy pierwszej spacji
"Kup mleko".lower()              # "kup mleko"
"exit".startswith("ex")          # True
```

`split(" ", 1)` z drugim argumentem ogranicza liczbę podziałów — przydaje
się, gdy reszta linii (np. treść zadania) ma zostać razem, mimo że sama
zawiera spacje.
