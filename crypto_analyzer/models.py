
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Coin:
    id: str
    symbol: str
    name: str
    current_price: float
    price_change_percentage_24h: float | None
    market_cap: int
    total_volume: float
    last_updated: datetime

    @classmethod
    def from_dict(cls, data: dict) -> "Coin":
        return cls(
            id=data["id"],
            symbol=data["symbol"],
            name=data["name"],
            current_price=data["current_price"],
            price_change_percentage_24h=data["price_change_percentage_24h"],
            market_cap=data["market_cap"],
            total_volume=data["total_volume"],
            last_updated=datetime.fromisoformat(data["last_updated"].replace("Z", "+00:00"))
        )
    
    def __str__(self) -> str:
        return (
            f"id: {self.id}\n"
            f"symbol: {self.symbol}\n"
            f"name: {self.name}\n"
            f"price: {self.current_price}\n"
            f"change 24h: {self.price_change_percentage_24h}\n"
            f"market cap: {self.market_cap}\n"
            f"volume: {self.total_volume}\n"
            f"updated: {self.last_updated.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        )

    __repr__ = __str__
