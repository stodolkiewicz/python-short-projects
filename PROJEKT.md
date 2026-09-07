# Projekty edukacyjne

---

## Projekt 2: Crypto Analyzer

Pobieramy dane o kryptowalutach z CoinGecko API (darmowe, bez klucza), przetwarzamy przez struktury danych, wyświetlamy statystyki.

**Folder:** `crypto_analyzer/` (obok `expense_tracker/`)

**Co aplikacja robi:**
- pobiera top 20 kryptowalut z CoinGecko API async
- grupuje po kategorii/platformie → `defaultdict`
- liczy ile jest powyżej/poniżej średniej ceny → `Counter`
- deduplikuje platformy → `set`
- sortuje po zmianie 24h → `sorted` z `key=` i `lambda`
- pokazuje top 5 wzrostów i top 5 spadków → slicing
- parsuje odpowiedź do dataclassów → `@dataclass`
- wszystko async → `async/await`
- testy z mockowanym API → `unittest.mock`

**Pipeline:** `HTTP request (async) → JSON → dict → przetwarzanie strukturami → dataclass → output`

**Co ćwiczymy:** `async/await`, `asyncio`, `@dataclass`, `dict`/`list`/`set` głębiej, `defaultdict`, `Counter`, `json`, `try/except`, type hints (`Optional`, `Any`), `with`, comprehensions, `sorted` z `lambda`, slicing, `unittest.mock`.

---

## Projekt 3: GitHub Activity Analyzer

Pobieramy przez GitHub API własną aktywność i repozytoria, agregujemy i wyświetlamy statystyki.

**Co ćwiczymy:** `async/await`, `@dataclass`, `defaultdict` (grupowanie po języku), `Counter` (commity per dzień), `set` (deduplicacja tagów), `sorted` z `key=` i `lambda`, `datetime`, slicing (top N), `zip`, generatory (paginacja API), `unittest.mock` (testy z mockowanym API), `pathlib`, `json`.

**Pipeline:** `GitHub API (async, paginacja) → JSON → dataclassy → agregacja strukturami → statystyki → display`

---

---

# Projekt 1: Expense Tracker — plan projektu ✅

Piszemy aplikację do śledzenia wydatków. Tworzysz obiekty w kodzie,
wywołujesz metody, widzisz wyniki w terminalu.

---

## Jak to będzie działać

Wydatki tworzymy bezpośrednio w kodzie, jak w Javie `new Obiekt()`. Brak CLI, brak plików — wszystko żyje w pamięci.

Mamy dwie klasy: `expense.py` (jeden wydatek) i `Tracker` (kolekcja wydatków z metodami).

`Tracker` umie:
- `add` — dodaj wydatek
- `list` — wypisz wszystkie w tabeli (ID, kwota, kategoria, opis)
- `summary` — podsumowanie per kategoria + łączna suma
- `delete` — usuń po ID

---

## Struktura projektu

```
first-project/
  main.py           ← punkt wejścia, tu tworzysz obiekty i wywołujesz metody
  expense.py        ← klasa Expense (jeden wydatek)
  tracker.py        ← klasa Tracker: add, list, delete, summary
  PROJEKT.md        ← ten plik
```

---

## Kolejność implementacji

| Krok | Co dodajemy                          | Python którego ćwiczymy               |
|------|--------------------------------------|---------------------------------------|
| 1    | Klasa `expense.py`                       | klasy, `__init__`, `__str__`, `__repr__` |
| 2    | Klasa `Tracker` — add, list           | klasy, `list`, `for`, f-strings       |
| 3    | Metoda `delete`                       | indeksy, wyjątki                      |
| 4    | Metoda `summary`                      | `defaultdict`, `Counter`, sortowanie  |
| 5    | Walidacja pól (`amount > 0`, `description` niepusty) — `InvalidExpenseException` z domyślną wiadomością w `__init__`; opcjonalnie `try/except` w `main.py` | własne wyjątki, `super().__init__`, `try/except` |
| 6    | Filtrowanie po kategorii              | list comprehensions                   |
| 7    | `dataclass` refactor                  | `@dataclass`, type hints              |
| 8    | Testy                                 | `pytest`, asercje, fixtures           |
