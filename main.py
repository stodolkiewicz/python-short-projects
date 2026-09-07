import asyncio

from crypto_analyzer.analyzer import CryptoAnalyzer
from crypto_analyzer.client import CryptoClient
from crypto_analyzer.models import Coin
from expense_tracker.category import Category
from expense_tracker.expense import Expense
from expense_tracker.Tracker import Tracker
from task_manager.cli import run


def project1():
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

async def project2():
    crypto_client = CryptoClient()
    coins: list[Coin] = await crypto_client.get_top_cryptos(limit=10)

    crypto_analyzer = CryptoAnalyzer()
    
    top_gainers = crypto_analyzer.top_gainers(coins, limit=5)
    top_losers = crypto_analyzer.top_losers(coins, limit=5)
    # print()
    above_below = crypto_analyzer.above_below_average(coins)
    # print(above_below)

    # print(crypto_analyzer.group_by_symbol_prefix(coins))
    # print(crypto_analyzer.unique_first_letters(coins))

    print(crypto_analyzer.top_gainer_and_loser(coins))

def project3():
    run()


def main():
    # asyncio.run(project2())

    project3()

if __name__ == "__main__":
    main()
