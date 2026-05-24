from expense_tracker.Category import Category
from expense_tracker.InvalidExpenseException import InvalidExpenseException


class Expense:
    def __init__(self, amount: float, category: Category, description: str):
        if amount <= 0:
            raise InvalidExpenseException()
        
        self.amount = amount
        self.category = category
        self.description = description

    def __str__(self):
        return f"{self.category} - {self.description}: {self.amount}"
    
    def __repr__(self):
        return f"{self.category} - {self.description}: {self.amount}"