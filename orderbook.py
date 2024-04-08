import logging
from functools import reduce

from utils import get_data

logger = logging.getLogger(__name__)


def merge_orderbooks(a: list[list], b: list[list], reverse: bool = False) -> list[list]:
    a, b = dict(a), dict(b)
    for price, amount in b.items():
        a.setdefault(price, 0)
        a[price] += amount

    return list(sorted([list(i) for i in a.items()], key=lambda i: i[0], reverse=reverse))


def calculate_arbitrage(orderbooks):
    # assumes orderbook is a list of tuples like: [(price, volume), ...]
    # and they're sorted in ascending order
    profits = []
    asks = reduce(lambda l, r: merge_orderbooks(l, r), map(lambda book: book["asks"], orderbooks))
    bids = reduce(lambda l, r: merge_orderbooks(l, r, True), map(lambda book: book["bids"], orderbooks))
    for ask_price, ask_amount in asks:
        for bid in bids:
            if ask_price > bid[0] or ask_amount == 0 or bid[1] == 0:
                break
            delta = min(ask_amount, bid[1])
            profits.append(delta * (bid[0] - ask_price))
            ask_amount -= delta
            bid[1] -= delta
    # TODO: find total profit
    return sum(profits)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    SYMBOL = "QRDO-USDT"
    EXCHANGES = ["kucoin", "gateio", "mexc", "bitmart", "hitbtc", "bitfinex", "bitget"]
    data = get_data("fetch_order_book", SYMBOL, EXCHANGES)
    logger.info("Total possible profit %s", calculate_arbitrage(data.values()))
