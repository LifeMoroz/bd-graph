import datetime

import ccxt
import logging
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

SYMBOL = "QRDO-USDT"
EXCHANGES = ["kucoin", "gateio", "mexc", "bitmart", "hitbtc", "bitfinex", "bitget"]


symbol_variances = [SYMBOL, SYMBOL.replace("-", "_"), SYMBOL.replace("-", "")]

data = {}
for exchange_id in EXCHANGES:
    exchange = getattr(ccxt, exchange_id)()
    for variance in symbol_variances:
        try:
            data[exchange_id] = exchange.fetch_ohlcv(variance, timeframe="1m", limit=100)
            break
        except Exception as e:
            pass
    else:
        logger.error("Can't fetch %s ohlcv for %s", SYMBOL, exchange_id)


start_point = max(o[0][0] for o in data.values())
data = {k: list(filter(lambda o: o[0] >= start_point, candles)) for k, candles in data.items()}

plt.figure(figsize=(14, 7))
for exchange, candles in data.items():
    plt.plot(
        [datetime.datetime.utcfromtimestamp(c[0] / 1000) for c in candles], [c[-2] for c in candles], label=exchange
    )

plt.title(f"{SYMBOL} Price Chart")
plt.legend()
plt.show()
