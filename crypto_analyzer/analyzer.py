from collections import Counter, defaultdict

from crypto_analyzer.models import Coin


class CryptoAnalyzer:

    def top_gainers(self, coins: list[Coin], limit: int = 5) -> list[Coin]:
        sorted_coins = sorted(coins, key=lambda c: c.price_change_percentage_24h or 0, reverse=True)

        return sorted_coins[:limit]

    def top_losers(self, coins: list[Coin], limit: int = 5) -> list[Coin]:
        sorted_coins = sorted(coins, key=lambda c: c.price_change_percentage_24h or 0)

        return sorted_coins[:limit]

    def above_below_average(self, coins: list[Coin]) -> dict[str, int]:
        avg = sum(c.current_price for c in coins) / len(coins)
        result = {
            "above": 0,
            "below": 0
        }

        for coin in coins:
            if coin.current_price > avg:
                result["above"] += 1
            elif coin.current_price < avg:
                result["below"] += 1
        
        return result
    
    def group_by_symbol_prefix(self, coins: list[Coin]) -> defaultdict[str, list[Coin]]:
        d = defaultdict(list)
        
        for c in coins:
            d[c.name[0]].append(c)
            
        return d
    
    def unique_first_letters(self, coins: list[Coin]) -> set[str]:
        # unique_firt_name_letters = set([c.name[0] for c in coins])
        unique_firt_name_letters = {c.name[0] for c in coins}
        return unique_firt_name_letters
    
    def top_gainer_and_loser(self, coins: list[Coin]) -> tuple[Coin, Coin]:
        coins = [c for c in coins if c.price_change_percentage_24h is not None]
        gainer_to_loser = sorted(coins, key=lambda u : u.price_change_percentage_24h or 0, reverse=True)
        gainer = gainer_to_loser[0]
        loser = gainer_to_loser[-1]

        return (gainer, loser)