
from datetime import datetime

import pytest

from crypto_analyzer.analyzer import CryptoAnalyzer
from crypto_analyzer.models import Coin


@pytest.fixture
def coins() -> list[Coin]:
    now = datetime.now()
    return [
        Coin(id="a", symbol="a", name="A", current_price=100, price_change_percentage_24h=5.0,  market_cap=1000, total_volume=100, last_updated=now),
        Coin(id="b", symbol="b", name="B", current_price=200, price_change_percentage_24h=2.0,  market_cap=2000, total_volume=200, last_updated=now),
        Coin(id="c", symbol="c", name="C", current_price=300, price_change_percentage_24h=-1.0, market_cap=3000, total_volume=300, last_updated=now),
        Coin(id="d", symbol="d", name="D", current_price=400, price_change_percentage_24h=-3.0, market_cap=4000, total_volume=400, last_updated=now),
        Coin(id="e", symbol="e", name="E", current_price=500, price_change_percentage_24h=None, market_cap=5000, total_volume=500, last_updated=now),
    ]

def test_top_gainers(coins):
    crypto_analyzer = CryptoAnalyzer()
    top_gainers: list[Coin] = crypto_analyzer.top_gainers(coins, limit=3)

    assert any(c.price_change_percentage_24h == 5.0 for c in top_gainers)
    assert any(c.price_change_percentage_24h == 2.0 for c in top_gainers)


def test_top_gainers_respects_limit(coins):
    crypto_analyzer = CryptoAnalyzer()
    result = crypto_analyzer.top_gainers(coins, limit=2)

    assert len(result) == 2


def test_top_gainers_sorted_descending(coins):
    crypto_analyzer = CryptoAnalyzer()
    result = crypto_analyzer.top_gainers(coins, limit=3)

    changes = [c.price_change_percentage_24h or 0 for c in result]
    assert changes == sorted(changes, reverse=True)


def test_top_gainers_handles_none(coins):
    crypto_analyzer = CryptoAnalyzer()
    result = crypto_analyzer.top_gainers(coins, limit=5)

    assert all(c.id != "e" or c.price_change_percentage_24h is None for c in result)
