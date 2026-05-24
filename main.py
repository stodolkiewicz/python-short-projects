from expense_tracker.Category import Category
from expense_tracker.Expense import Expense
from expense_tracker.Tracker import Tracker


def main():
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
    

    # tracker.list()
    # tracker.remove(1)
    # tracker.list()
    # tracker.summary()
    
    tracker.list_by_category(Category.ENTERTAINMENT)

if __name__ == "__main__":
    main()
