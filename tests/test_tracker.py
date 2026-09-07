import pytest

from expense_tracker.category import Category
from expense_tracker.expense import Expense
from expense_tracker.Tracker import Tracker

@pytest.fixture
def tracker():
    tracker = Tracker()

    food_expense = Expense(
        category=Category.FOOD,
        description="hot dog",
        amount=3.50)
    
    house_expense = Expense(
        category=Category.HOUSING,
        description="rent",
        amount=2500
    )

    entertainment_expense1 = Expense(
        category=Category.ENTERTAINMENT,
        description="Netflix",
        amount=19.99
    )

    entertainment_expense2 = Expense(
        category=Category.ENTERTAINMENT,
        description="Udemy Course",
        amount=9.99
    )

    tracker.add(food_expense)
    tracker.addAll(house_expense, entertainment_expense1, entertainment_expense2)

    return tracker

def test_something(tracker):
    entertainments: list[Expense] = tracker.list_by_category(Category.ENTERTAINMENT)
    assert len(entertainments) == 2
    assert any(e.amount == 9.99 and e.description == "Udemy Course" for e in entertainments)