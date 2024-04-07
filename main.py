import datetime
import logging
from collections import defaultdict

import matplotlib.pyplot as plt

from utils import get_data

logger = logging.getLogger(__name__)

RESOLUTION = "1m"


def plot(symbol: str, data: dict):
    plt.figure(figsize=(14, 7))
    for exchange, candles in data.items():
        plt.plot(
            [datetime.datetime.utcfromtimestamp(c[0] / 1000) for c in candles], [c[-2] for c in candles], label=exchange
        )

    plt.title(f"{symbol} Price Chart")
    plt.legend()
    plt.show()


def run(symbol, exchanges, start: datetime.datetime, end: datetime.datetime):
    data = defaultdict(list)
    while start and end and start < end:
        _end = min(start + datetime.timedelta(minutes=100), end)
        logger.info("Fetching data for [%s, %s)", start, _end)
        _data = get_data(
            "fetch_ohlcv",
            symbol,
            exchanges,
            timeframe=RESOLUTION,
            limit=100,
            since=int(start.timestamp() * 1000),
            params={"until": int(_end.timestamp() * 1000)},
        )
        for k, v in _data.items():
            if v:
                data[k] += v
        start = _end
    start_point = max(o[0][0] for o in data.values())
    end_point = end.timestamp() * 1000
    data = {
        k: list(sorted(filter(lambda o: end_point >= o[0] >= start_point, candles), key=lambda o: o[0]))
        for k, candles in data.items()
    }
    plot(symbol, data)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    SYMBOL = "QRDO-USDT"
    EXCHANGES = ["kucoin", "gateio", "mexc", "bitmart", "hitbtc", "bitfinex", "bitget"]
    # [start, end)
    START = datetime.datetime(2024, 4, 2, 0, 0)
    END = datetime.datetime(2024, 4, 2, 4, 0)

    run(SYMBOL, EXCHANGES, START, END)
