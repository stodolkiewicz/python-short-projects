from task_manager.task import Task



def add_task(tasks: list[Task], arg: str) -> None:
    """Add a task"""
    tasks.append(
        Task(
            id = max([t.id for t in tasks], default=0) + 1,
            description = arg
        )
    )

def list_tasks(tasks: list[Task], arg: str) -> None:
    """List tasks"""
    for task in tasks:
        print(task)

    if len(tasks) == 0:
        print("No tasks created yet.")

def done_task(tasks: list[Task], arg: str) -> None:
    """Switch the task to done"""
    try:
        int_arg = int(arg)
        task_found = False

        for task in tasks:
            if task.id == int_arg:
                task.done = True
                task_found = True

        if not task_found:
            print("id does not exist")

    except ValueError:
        print("Invalid value")

def remove_task(tasks: list[Task], arg: str) -> None:
    """Remove the task with given id"""
    try:
        int_arg = int(arg)
        task_to_remove = next((t for t in tasks if t.id == int_arg), None)

        if task_to_remove is not None:
            tasks.remove(task_to_remove)
    except ValueError:
        print("Invalid value")

def help_command(tasks: list[Task], arg: str) -> None:
    """Print available commands"""
    for name, func in COMMANDS.items():
        print(f"{name}: {func.__doc__}")

COMMANDS = {
    "add": add_task,
    "list": list_tasks,
    "done": done_task,
    "remove": remove_task,
    "help": help_command
}