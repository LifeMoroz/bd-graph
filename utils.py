import logging

import ccxt


logger = logging.getLogger(__name__)


def symbol_variances(symbol: str):
    return [symbol, symbol.replace("-", "_"), symbol.replace("-", "")]


def get_data(method: str, symbol: str, exchanges: list[str]):
    data = {}
    for exchange_id in exchanges:
        exchange = getattr(ccxt, exchange_id)()
        for variance in symbol_variances(symbol):
            try:
                data[exchange_id] = getattr(exchange, method)(variance)
                break
            except Exception:
                pass
        else:
            logger.error("Can't fetch %s ohlcv for %s", symbol, exchange_id)
    return data
