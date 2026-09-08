# `uv` — menedżer pakietów i środowisk

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

## Extras — `uv add pydantic[email]`

Nawiasy kwadratowe po nazwie paczki to nie składnia Pythona, tylko konwencja
menedżerów pakietów (pip, uv, PEP 508) — nazywa się **extras**. Wiele
bibliotek ma opcjonalne zależności, które nie są instalowane domyślnie, bo
nie każdy ich potrzebuje.

```bash
uv add pydantic[email]
```

To instaluje `pydantic` razem z dodatkową paczką `email-validator`, potrzebną
do typu `EmailStr`. Bez `[email]` sam `pydantic` się zainstaluje, ale
`EmailStr` nie zadziała — brakowałoby zależności, którą waliduje adresy
e-mail.

Można podać kilka extras naraz: `pydantic[email,timezone]`. Autor paczki sam
definiuje, jakie nazwy extras istnieją i co każda z nich instaluje — to nie
jest coś uniwersalnego, wspólnego dla każdej biblioteki.

---

## Uruchamianie projektu

```bash
uv run main.py
```
