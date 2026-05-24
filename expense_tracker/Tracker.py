from expense_tracker.Category import Category
from expense_tracker.Expense import Expense


class Tracker:


    def __init__(self):
        self.expenses: list[Expense] = []

    def add(self, expense: Expense):
        self.expenses.append(expense)

    def addAll(self, *expenses: list[Expense]):
        self.expenses.extend(expenses)

    def listAll(self):
        for index, expense in enumerate(self.expenses):
            print(f"{index}. {expense}")
            
    def remove(self, index: int) -> Expense:
        self.expenses.pop(index)

    def summary(self):
        total_expenses = 0
        cat_to_value = {}

        for expense in self.expenses:
            total_expenses += expense.amount
            # sprawdz czy kategoria istnieje juz w dict
            if expense.category in cat_to_value:
                previous_total_for_category = cat_to_value[expense.category]
                cat_to_value[expense.category] = previous_total_for_category + expense.amount
            else:
                cat_to_value[expense.category] = expense.amount

        # wypisywanie
        for category in cat_to_value:
            print(f"{category.name}      ", end="")
            print(f"{cat_to_value[category]:.2f}")

        print("--------------")
        print(f"TOTAL:      {total_expenses:.2f}")

    def list_by_category(self, category: Category) -> list[Expense]:
        items_by_category = [e for e in self.expenses if e.category == category]
        print(items_by_category)
        return items_by_category
