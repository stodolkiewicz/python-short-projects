import json
from dataclasses import asdict

from task_manager.task import Task


def save_tasks(tasks: list[Task]) -> None:
    with open("./task_manager/local_db/tasks.json", "w") as f:
        json_tasks = [asdict(task) for task in tasks]
        json.dump(json_tasks, f)

def load_tasks() -> list[Task]:
    try:
        with open("./task_manager/local_db/tasks.json") as f:
            data = json.load(f)
            return [Task(**json_task) for json_task in data]
    except FileNotFoundError:
        return []
