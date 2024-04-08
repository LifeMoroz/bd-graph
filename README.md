## Install

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# Configure

```python
# ./main.py
# Set SYMBOL
SYMBOL = "QRDO-USDT"
# Set EXCHANGES
EXCHANGES = ["kucoin", "gateio", "mexc", "bitmart", "hitbtc", "bitfinex", "bitget"]
```

## Run

```shell
# Activate venv if required
# source .venv/bin/activate
# Print price graph
python main.py
# Print possible orderbook profit
python orderbook.py
```