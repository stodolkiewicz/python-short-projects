from task_manager import storage
from task_manager.commands import COMMANDS
from task_manager.task import Task


def parse_command(line: str) -> tuple[str, str]:
    # 1 -> max podziałów
    parts: list[str] = line.strip().split(" ", 1)
    return parts[0], parts[1] if len(parts) == 2 else ""

def run():
    tasks: list[Task] = storage.load_tasks()

    while(line := input("> ")).strip() != "exit":
        name, arg = parse_command(line)

        if name in COMMANDS:
            COMMANDS[name](tasks, arg)
        else:
            print("unknown command")

    storage.save_tasks(tasks)