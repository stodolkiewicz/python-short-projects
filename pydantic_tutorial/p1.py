from datetime import datetime, UTC
from functools import partial
from typing import Literal, Annotated

from uuid import UUID, uuid4

from pydantic import (
    BaseModel,
    ValidationError,
    Field,
    EmailStr,
    HttpUrl,
    SecretStr,
    field_validator,
    model_validator,
    ValidationInfo,
    computed_field
)

class User(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    # uid: Annotated[int, Field(gt=0)]
    username: Annotated[str,Field(min_length=3, max_length=20)]
    email: EmailStr
    first_name: str
    last_name: str
    follower_count: int = 0
    website: HttpUrl | None = None
    password: SecretStr
    age: Annotated[int, Field(ge=13, le=130)]
    verified_at: datetime | None = None
    bio: str = ""
    is_active: bool = True
    full_name: str | None = None

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.replace("_", "").isalnum():
            raise ValueError("Username must be alphanumeric (underscores allowed)")
        return v.lower()

    # sprawdza czy zaczyna sie od https / http a jak nie to dodaje na poczatku
    @field_validator("website", mode="before")
    @classmethod
    def add_https(cls, v: str | None) -> str | None:
        if v and not v.startswith(("http://", "https://")):
            return f"https://{v}"
        return v

    @computed_field
    @property
    def display_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"

    @computed_field
    @property
    def is_influencer(self) -> bool:
        return self.follower_count >= 10000

def run():
    try:
        user = User(
            uid="123",
            username="DAW_id",
            first_name="john",
            last_name="doe",
            email="stoso@gmail.com",
            age=22,
            password="secret123123",
            website="hsttp://coadsoas"
        )

        # domyślnie - brak walidacji po stworzeniu!
        # user.bio = "Python Developer"
        # print(user.model_dump_json(indent=2))
        # print(user.password.get_secret_value())
        print(user)

    except ValidationError as e:
        print(e)


class Comment(BaseModel):
    content: str
    author_email: EmailStr
    likes: int = 0

class BlogPost(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=200)]
    content: Annotated[str, Field(min_length=10)]
    author: User
    view_count: int = 0
    is_published: bool = False
    tags: list[str] = Field(default_factory=list)
    # ustawiłoby czas kiedy klasa jest definiowana dla wszystkich BlogPost !!! -> źle!!!
    # create_at: datetime.now(UTC)
    # works
    create_at: datetime = Field(default_factory= lambda: datetime.now(tz=UTC))
    # also works - partial returns unexecuted function (of datetime with arg tz=UTC)
    create_at: datetime = Field(default_factory=partial(datetime.now, tz=UTC))
    author_id: str | int
    status: Literal["draft", "published", "archived"] = "draft"
    slug: Annotated[str, Field(pattern=r"^[a-z0-9-]+$")]
    comments: list[Comment] = Field(default_factory=list)

def run2():
    post = BlogPost(
        title="Getting started with Python",
        content="Here's, how to begin..,",
        author_id="12345"
    )

    print(post)


class UserRegistration(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

    @model_validator(mode = "after")
    def passwords_match(self) -> "UserRegistration":
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self

def run3():
    try:
        registration = UserRegistration(
            email="dawid@gmail.com",
            password="secret123",
            confirm_password="secret123"
        )
    except ValidationError as e:
        print(e)









