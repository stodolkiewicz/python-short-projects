from typing import Any
from crypto_analyzer.models import Coin

import httpx
import asyncio


class CryptoClient:
    async def get_top_cryptos(self, limit: int = 3) -> list[Coin]:
        url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&per_page={limit}"
    
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            # throws exception for 4xx 5xx
            response.raise_for_status()
            
            jsons: list[dict[str, Any]] =  response.json()

            return [Coin.from_dict(json) for json in jsons]
