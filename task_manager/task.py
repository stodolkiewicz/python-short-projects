from dataclasses import dataclass


@dataclass
class Task:
    id: int
    description: str
    done: bool = False

    def __str__(self) -> str:
        status = "✓" if self.done else " "
        return f"{self.id}. [{status}] {self.description}"
