# Pydantic

Notatki z nauki Pydantic w `pydantic_tutorial/`.

---

## `BaseModel` — walidowana klasa danych

Klasa dziedzicząca po `BaseModel` sprawdza typy pól przy tworzeniu instancji
i rzuca `ValidationError`, jeśli przekazana wartość nie pasuje. To różni ją
od `@dataclass`, który niczego nie sprawdza — przyjmie każdą wartość, nawet
złego typu.

```python
from pydantic import BaseModel, ValidationError

class User(BaseModel):
    username: str
    email: str

try:
    user = User(username="dawid", email=123)   # email ma być str, nie int
except ValidationError as e:
    print(e)
```

Walidacja dzieje się tylko przy tworzeniu obiektu. Przypisanie do już
istniejącego atrybutu (`user.bio = "..."`) domyślnie nic nie sprawdza.

---

## `Annotated` + `Field` — dodatkowe ograniczenia na pole

`Field` pozwala dopisać do typu reguły, których sam type hint nie wyrazi —
np. że liczba ma być dodatnia, albo że string ma konkretną długość.
`Annotated[typ, Field(...)]` to sposób na doczepienie takich reguł do
konkretnego typu w adnotacji pola.

```python
from typing import Annotated
from pydantic import BaseModel, Field

class User(BaseModel):
    uid: Annotated[int, Field(gt=0)]
    username: Annotated[str, Field(min_length=3, max_length=20)]
    age: Annotated[int, Field(ge=13, le=130)]
```

`gt`/`ge` to "greater than"/"greater or equal", `lt`/`le` to odpowiedniki
dla góry zakresu — nazwy przejęte wprost z matematycznych symboli `>`, `>=`,
`<`, `<=`.

---

## `Literal` vs `Enum`

`Literal["draft", "published", "archived"]` ogranicza wartość do zamkniętego
zbioru stringów (albo innych stałych), ale nie tworzy żadnej klasy — w
runtime `status` to zwykły `str`, np. `"draft"`. `Literal` działa na
poziomie typowania i walidacji, nie daje Ci obiektu z `.name`/`.value` tak
jak `Enum`.

```python
from typing import Literal

class BlogPost(BaseModel):
    status: Literal["draft", "published", "archived"] = "draft"
```

`Literal` ma sens, gdy potrzebujesz tylko walidacji zbioru stringów. `Enum`
ma sens, gdy chcesz też metody, iterację po wartościach, albo używać tego
jako właściwy typ w wielu miejscach kodu.

---

## `default_factory` — wartość domyślna liczona przy każdym utworzeniu

Zwykła wartość domyślna (`= []`, `= datetime.now(UTC)`) liczy się **raz**,
w momencie definiowania klasy — wszystkie instancje dostałyby tę samą listę
albo ten sam moment w czasie. `default_factory` przyjmuje funkcję bez
argumentów, którą Pydantic wywołuje osobno dla każdej nowej instancji.

```python
from datetime import datetime, UTC
from functools import partial

class BlogPost(BaseModel):
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
```

`partial(datetime.now, tz=UTC)` robi to samo co `lambda: datetime.now(tz=UTC)`
— przygotowuje wywołanie `datetime.now(tz=UTC)`, ale odkłada jego wykonanie
na później, zamiast wołać je od razu.

`Field(default_factory=uuid4)` działa tym samym mechanizmem, tylko z
`uuid4` z modułu `uuid` — każda instancja dostaje świeżo wygenerowany,
unikalny identyfikator zamiast jednego wspólnego:

```python
from uuid import UUID, uuid4

class User(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
```

---

## Specjalne typy do walidacji konkretnych formatów

Pydantic ma gotowe typy dla popularnych formatów danych, zamiast `str` plus
ręczna walidacja regexem.

```python
from pydantic import EmailStr, HttpUrl, SecretStr

class User(BaseModel):
    email: EmailStr        # musi być poprawnym adresem e-mail
    website: HttpUrl        # musi być poprawnym URL-em, Pydantic go też parsuje
    password: SecretStr     # wartość zamaskowana w print()/repr(), żeby nie wyciekła do logów
```

`EmailStr` wymaga extras `pydantic[email]` — bez tego dostaniesz błąd importu
(masz to opisane w `uv.md`). `SecretStr` chowa wartość — `print(user.password)`
pokaże coś w stylu `SecretStr('**********')`, a prawdziwą wartość dostajesz
dopiero przez `user.password.get_secret_value()`.

---

## `Field(pattern=...)` — walidacja regexem

```python
slug: Annotated[str, Field(pattern=r"^[a-z0-9-]+$")]
```

Wartość musi pasować do podanego wyrażenia regularnego, inaczej `ValidationError`.
Przydatne, gdy żaden gotowy typ (jak `EmailStr`) nie pokrywa formatu, którego
potrzebujesz.

---

## `@field_validator` — własna walidacja pojedynczego pola

Gdy reguła jest zbyt specyficzna dla `Field(...)` (np. transformacja
wartości, nie tylko sprawdzenie), piszesz własną funkcję walidującą.

```python
from pydantic import field_validator

class User(BaseModel):
    username: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.replace("_", "").isalnum():
            raise ValueError("Username must be alphanumeric (underscores allowed)")
        return v.lower()
```

`v` to wartość pola po podstawowej walidacji typu. Funkcja albo zwraca
(ewentualnie zmienioną) wartość, która trafia do modelu, albo rzuca
`ValueError`, co Pydantic zamienia na `ValidationError`. `@classmethod` jest
tu wymagane — Pydantic wywołuje tę funkcję na poziomie klasy, nie instancji.

Domyślnie walidator dostaje wartość **po** konwersji typu. `mode="before"`
uruchamia go na surowej wartości wejściowej, zanim Pydantic w ogóle spróbuje
jej przypasować typ — przydatne, gdy chcesz naprawić dane przed walidacją,
a nie tylko je sprawdzić:

```python
@field_validator("website", mode="before")
@classmethod
def add_https(cls, v: str | None) -> str | None:
    if v and not v.startswith(("http://", "https://")):
        return f"https://{v}"
    return v
```

---

## `@model_validator` — walidacja na poziomie całego modelu

Gdy reguła dotyczy kilku pól naraz (np. "hasło musi się zgadzać z
potwierdzeniem hasła"), `@field_validator` nie wystarczy, bo działa na
jednym polu. `@model_validator(mode="after")` dostaje dostęp do całego już
zbudowanego obiektu przez `self`:

```python
from pydantic import model_validator

class UserRegistration(BaseModel):
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def passwords_match(self) -> "UserRegistration":
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
```

Funkcja musi zwrócić `self` — to on staje się finalnym, zwalidowanym
obiektem.

---

## `@computed_field` — pole liczone, widoczne w serializacji

Zwykły `@property` jest widoczny tylko w Pythonie — nie pojawi się w
`model_dump()` ani `model_dump_json()`. `@computed_field` nad `@property`
dodaje tę wartość do wyniku serializacji, mimo że nie jest to prawdziwe pole
modelu, tylko coś policzonego z innych pól:

```python
from pydantic import computed_field

class User(BaseModel):
    first_name: str
    last_name: str

    @computed_field
    @property
    def display_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
```

`user.model_dump()` zwróci wtedy też klucz `display_name`, mimo że nigdy go
nie ustawiałeś przy tworzeniu obiektu.

---

## Zagnieżdżone modele

Pole może mieć typ innego `BaseModel` — Pydantic waliduje wtedy zagnieżdżony
obiekt rekurencyjnie, tymi samymi zasadami co model najwyższego poziomu.

```python
class Comment(BaseModel):
    content: str
    author_email: EmailStr

class BlogPost(BaseModel):
    author: User
    comments: list[Comment] = Field(default_factory=list)
```

Jeśli `comments` dostanie listę słowników zamiast listy `Comment`, Pydantic
sam spróbuje każdy z nich zbudować i zwalidować jako `Comment`.

---

## `X | None` bez `= None` to wciąż pole wymagane

`X | None` opisuje tylko dozwolony **typ** pola — że oprócz `X` wolno podać
też `None`. To nie ustawia wartości domyślnej. Bez `= None` na końcu pole
nadal jest wymagane, tylko dodatkowo akceptuje `None` jako jedną z
poprawnych wartości.

```python
verified_at: datetime | None = None    # opcjonalne — ma wartość domyślną
website: HttpUrl | None                # wymagane — brak wartości domyślnej
```

---

## `Field(alias=...)` — inna nazwa pola na zewnątrz

Dane wejściowe (np. JSON z jakiegoś API) często używają innej konwencji
nazewnictwa niż Twój kod — `camelCase` zamiast `snake_case`, albo zupełnie
inna nazwa. `alias` mówi Pydantic, pod jaką nazwą szukać wartości dla tego
pola przy tworzeniu obiektu, niezależnie od tego, jak pole nazywa się w
Pythonie.

```python
class User(BaseModel):
    username: str = Field(alias="userName")

user = User(userName="dawid")   # trzeba użyć aliasu, nie nazwy pola
user.username                   # "dawid" — w Pythonie i tak odwołujesz się przez username
```

Domyślnie, gdy pole ma `alias`, konstruktor przyjmuje **tylko** tę nazwę —
`User(username="dawid")` rzuci błąd, bo formalną nazwą do budowania obiektu
stał się `userName`. To dlatego istnieje `populate_by_name` w `ConfigDict`
poniżej — pozwala zaakceptować obie nazwy naraz.

---

## `ConfigDict` — konfiguracja zachowania modelu

`model_config = ConfigDict(...)` ustawia zasady działające dla całego
modelu, zamiast per-pole. W Pydantic v1 służyła do tego zagnieżdżona klasa
`class Config:` — `ConfigDict` to jej odpowiednik w v2.

```python
from pydantic import BaseModel, ConfigDict, Field

class User(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        extra="allow",
        validate_assignment=True,
        frozen=True,
    )

    username: str = Field(alias="userName")
```

- **`populate_by_name`** — ma znaczenie tylko dla pól z `alias` (jak `username` powyżej, gdzie zewnętrzna nazwa to `userName`). Domyślnie taki model da się zbudować tylko przez alias: `User(userName="dawid")`, a `User(username="dawid")` rzuci błąd, bo `username` "formalnie" nazywa się `userName`. `populate_by_name=True` pozwala użyć obu nazw zamiennie.
- **`strict`** — wyłącza automatyczną konwersję typów przy walidacji. Domyślnie Pydantic działa w trybie "lax" i sam konwertuje pasujące typy — dlatego `User(uid="123", ...)` z Twojego wcześniejszego przykładu (gdzie `uid: Annotated[int, Field(gt=0)]`) przechodziło: string `"123"` został po cichu zamieniony na `int(123)`. Z `strict=True` taka wartość zostałaby odrzucona — pole `int` musi dostać prawdziwy `int`, nie string, który da się na niego zamienić.
- **`extra="allow"`** — nieznane pola przekazane do konstruktora nie są ani ignorowane (domyślne `"ignore"`), ani odrzucane (`"forbid"`), tylko dodawane do obiektu jako dodatkowe atrybuty, mimo że nie są zadeklarowane w klasie.
- **`validate_assignment=True`** — domyślnie Pydantic waliduje tylko przy tworzeniu obiektu; późniejsze przypisanie (`user.age = -5`) nic nie sprawdza. Ta opcja włącza walidację też przy każdym kolejnym przypisaniu do atrybutu.
- **`frozen=True`** — blokuje jakiekolwiek przypisanie do pól po utworzeniu obiektu; `user.username = "inna"` rzuci błąd zamiast zmienić wartość. Dodatkowo taki model staje się hashowalny (da się go np. wrzucić do `set`), czego zwykłe, mutowalne modele Pydantic nie umożliwiają.

---

## `@property` — metoda, która wygląda jak atrybut

`@property` pozwala napisać metodę, która wywołuje się bez nawiasów, tak jak
zwykły atrybut. Używa się tego, gdy wartość ma być policzona albo
zwalidowana przy dostępie, ale kod korzystający z klasy nie powinien o tym
wiedzieć.

```python
class Circle:
    def __init__(self, radius: float):
        self.radius = radius

    @property
    def area(self) -> float:
        return 3.14159 * self.radius ** 2

c = Circle(2)
c.area          # 12.566 — bez nawiasów, mimo że to metoda, liczona na bieżąco
```

Bez `@property` trzeba by zrobić `c.area()` (zwykła metoda) albo liczyć
`area` ręcznie za każdym razem, gdy `radius` się zmieni. Z `@property`
`c.area` jest zawsze aktualne, bo liczy się od nowa przy każdym odczycie.

Jest też `@area.setter`, który pozwala kontrolować przypisanie do `area`
(np. odrzucić wartość ujemną) — to osobny krok poza samym getterem powyżej.
