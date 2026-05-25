import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from crypto_analyzer.client import CryptoClient
from crypto_analyzer.models import Coin

SAMPLE_RESPONSE = [
    {
        "id": "bitcoin",
        "symbol": "btc",
        "name": "Bitcoin",
        "current_price": 76000.0,
        "price_change_percentage_24h": -0.5,
        "market_cap": 1500000000000,
        "total_volume": 20000000000,
        "last_updated": "2024-01-15T12:30:00.000Z",
    }
]


@pytest.mark.anyio
async def test_get_top_cryptos_returns_coins():
    mock_response = MagicMock()
    mock_response.json.return_value = SAMPLE_RESPONSE
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    with patch("crypto_analyzer.client.httpx.AsyncClient") as mock_class:
        mock_class.return_value.__aenter__.return_value = mock_client

        coins = await CryptoClient().get_top_cryptos(limit=1)

    assert len(coins) == 1
    assert coins[0].id == "bitcoin"
    assert isinstance(coins[0], Coin)
