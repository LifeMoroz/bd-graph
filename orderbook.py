import logging
from functools import reduce

from utils import get_data

logger = logging.getLogger(__name__)


def merge_orderbooks(a: list, b: list, reverse: bool = False):
    a, b = dict(a), dict(b)
    for price, amount in b.items():
        a.setdefault(price, 0)
        a[price] += amount

    return list(sorted(a.items(), key=lambda i: i[0], reverse=reverse))


def calculate_arbitrage(orderbooks):
    # assumes orderbook is a list of tuples like: [(price, volume), ...]
    # and they're sorted in ascending order
    profits = []
    asks = reduce(lambda l, r: merge_orderbooks(l, r), map(lambda book: book["asks"], orderbooks))
    bids = reduce(lambda l, r: merge_orderbooks(l, r, True), map(lambda book: book["bids"], orderbooks))
    # TODO: find total profit
    return profits


if __name__ == "__main__":
    SYMBOL = "QRDO-USDT"
    EXCHANGES = ["kucoin", "gateio", "mexc", "bitmart", "hitbtc", "bitfinex", "bitget"]
    data = get_data("fetch_order_book", SYMBOL, EXCHANGES)
    logger.info("Total possible profit %s", calculate_arbitrage(data.values()))
