# Python — do nauczenia

---

## Potrzebne do Google ADK

W tej kolejności.

- `async/await` — `async def`, `await`, `async for` — ADK jest prawie w całości async
- Docstringi — w ADK LLM czyta docstring żeby wiedzieć co robi tool; to nie jest opcjonalna dokumentacja
- Type hints: `Optional[str]`, `Any`, `dict[str, Any]` — sygnatury toolsów są nimi opisane
- Funkcje jako wartości — `tools=[get_stock_price]` — przekazywanie funkcji jak obiektów
- Walrus operator `:=` — pojawia się w ADK kodzie
- `try/except/else/finally`
- `@dataclass` — struktury danych w ADK
- `with` — context managers
- `json` — serialize/deserialize

---

## Podstawy których nie było

- `tuple` — niemutowalna lista, `(1, 2, 3)`
- Slicing: `lista[1:3]`, `lista[::2]`, `lista[::-1]`
- Unpacking: `a, b = 1, 2` / `first, *rest = lista`
- Ternary: `x if warunek else y`
- `is` vs `==` — tożsamość vs równość (jak `==` vs `.equals()` w Javie)
- Truthiness — `if lista:` zamiast `if len(lista) > 0:`
- `while` loop
- `break` / `continue`
- `range()` — `for i in range(10)`

## Stringi

- Metody: `split()`, `join()`, `strip()`, `upper()`, `lower()`, `startswith()`, `replace()`
- f-string zaawansowane: `{value!r}`, `{value:>10}`, `{value:0>5}`
- Multiline strings (`"""`)

## Kolekcje — głębiej

- `list`: `sort()`, `reverse()`, `index()`, `insert()`, `copy()`
- `dict`: `get()`, `items()`, `keys()`, `values()`, `update()`, `setdefault()`
- `set` — zbiór unikalnych wartości, operacje: `union`, `intersection`, `difference`
- `defaultdict` — dict który nie rzuca KeyError
- `Counter` — zliczanie wystąpień
- Comprehensions: słownikowe `{k: v for ...}`, zbiorowe `{x for ...}`

## Klasy i OOP

- `@property` — gettery/settery bez metod
- `@classmethod` / `@staticmethod`
- Magic methods: `__eq__`, `__hash__`, `__len__`, `__iter__`, `__contains__`
- `copy` vs `deepcopy` — referencje vs głęboka kopia

## Funkcje

- `lambda`
- `map()`, `filter()`
- `sorted()` z `key=`
- `zip()`
- `**kwargs`
- `functools.lru_cache`

## Generatory

- `yield`
- Generator expressions: `(x for x in lista)`
- `itertools`: `chain`, `groupby`, `product`

## Typowanie

- `Union[X, Y]` / `X | Y`
- `TypeVar` — generyki

## Testy

- `unittest.mock`
- `pytest.raises` — testowanie wyjątków
- `@pytest.mark.parametrize`

## Inne

- `match/case` — pattern matching (Python 3.10+)
- `datetime`
- `re` — wyrażenia regularne
- `os` / `sys`
- `pathlib.Path`

---

## Dla chętnych

Nie potrzebne do czytania ADK, ale warte poznania kiedyś.

- `Protocol` / `ABC` / `@abstractmethod` — duck typing i klasy abstrakcyjne
- `namedtuple` — lekka alternatywa dla prostych klas
- Closures i `nonlocal`
- Operator overloading — `__add__`, `__lt__`, `__eq__` itd.
- `bytes` i encoding — `encode()`, `decode()`, UTF-8
- `concurrent.futures` — `ThreadPoolExecutor`, `ProcessPoolExecutor`
- `__all__` w `__init__.py`
- `csv`
- Dekoratory — pisanie własnych z `functools.wraps`
- Deskryptory atrybutów (`__get__`, `__set__`) — jak działa `@property` pod spodem
- Metaklasy — jak działa `@dataclass` pod spodem
