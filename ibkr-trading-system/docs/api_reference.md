## Stage One Initialization

The `initialize_stage_one` function is designed to handle the initial setup and connection phase for the trading system. This includes connecting to Interactive Brokers, retrieving account information, and fetching sample market data.

### `initialize_stage_one(host, port, client_id, account_code, symbol, exchange, currency)`

**Location:** `ibkr-trading-system.src.stages.initialize_stage_one`

This function orchestrates the first stage of operations:

1.  **Establishes Connection**: Connects to Interactive Brokers TWS or Gateway using the provided `host`, `port`, and `client_id`.
2.  **Fetches Account Summary**: Retrieves account summary details for the given `account_code`. If the connection is not live or data cannot be fetched, it may return mock data.
3.  **Fetches Market Data**: Retrieves a market data snapshot for the specified `symbol` on the given `exchange` and in the specified `currency`.

**Parameters:**

*   `host (str)`: The host address for TWS or IB Gateway (default: '127.0.0.1').
*   `port (int)`: The port number for TWS or IB Gateway (default: 7497 for TWS paper).
*   `client_id (int)`: A unique client ID for the IB connection (default: 1).
*   `account_code (str)`: The IB account code for which to fetch a summary (default: "DU1234567").
*   `symbol (str)`: The stock symbol for which to fetch market data (default: 'AAPL').
*   `exchange (str)`: The exchange where the stock is traded (default: 'SMART').
*   `currency (str)`: The currency of the stock (default: 'USD').

**Returns:**

*   `Dict[str, Any]`: A dictionary containing the following keys:
    *   `'connection_status' (bool)`: True if connection to IB was successful, False otherwise.
    *   `'account_summary' (dict)`: A dictionary with account summary details. May contain mock data if the connection was not live or if there was an error.
    *   `'market_data' (dict | str | None)`: A dictionary with market data (last price, bid, ask, etc.) for the symbol if successful. Could be a string with an error message if data fetching failed, or None.
    *   `'error' (str | None)`: A string describing any major error that occurred during the process, or None if no major error.

**Example Usage (Conceptual):**

```python
from ibkr_trading_system.src.stages import initialize_stage_one

results = initialize_stage_one(
    host='127.0.0.1',
    port=7497, # TWS Paper Trading port
    client_id=25,
    account_code='YOUR_ACCOUNT_CODE',
    symbol='MSFT'
)

print(f"Connection Successful: {results['connection_status']}")
if results['account_summary']:
    print(f"Account Net Liquidation: {results['account_summary'].get('NetLiquidation')}")
if results['market_data'] and isinstance(results['market_data'], dict):
    print(f"MSFT Last Price: {results['market_data'].get('last_price')}")
if results['error']:
    print(f"Error: {results['error']}")
```

## Demo Notebook

A demonstration of the `initialize_stage_one` function can be found in the Jupyter notebook:
`ibkr-trading-system/notebooks/demo/stage_one_demo.ipynb`.

This notebook provides a step-by-step guide to:
- Setting up the Python environment.
- Calling `initialize_stage_one` with example parameters.
- Inspecting the returned results.

It is highly recommended to run this notebook to understand the behavior of Stage One and to test your connection setup with Interactive Brokers.
Remember to have TWS or IB Gateway running and configured for API access before executing the notebook.
