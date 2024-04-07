import logging

import ccxt


logger = logging.getLogger(__name__)


def get_data(method: str, symbol: str, exchanges: list[str], **kwargs):
    data = {}
    for exchange_id in exchanges:
        exchange = getattr(ccxt, exchange_id)()
        try:
            data[exchange_id] = getattr(exchange, method)(symbol.replace("-", "/"), **kwargs)
        except Exception as e:
            logger.warning("Failed to get data: %s", e)
    return data
