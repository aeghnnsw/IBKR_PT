from .connection.connection_manager import ConnectionManager
from ib_insync import Stock, Contract, IB # Added Contract
from typing import Dict, Any, Optional

def initialize_stage_one(
    host: str = '127.0.0.1',
    port: int = 7497,
    client_id: int = 1,
    account_code: str = "DU1234567", # Default/Example account code
    symbol: str = 'AAPL',
    exchange: str = 'SMART',
    currency: str = 'USD'
) -> Dict[str, Any]:
    """
    Implements Stage One: Connect to IB, get account summary, and fetch sample market data.

    Args:
        host (str): Host address for TWS/Gateway.
        port (int): Port number for TWS/Gateway.
        client_id (int): Client ID for the IB connection.
        account_code (str): Account code for which to fetch summary.
        symbol (str): Stock symbol for which to fetch market data (e.g., 'AAPL').
        exchange (str): The exchange for the stock (e.g., 'SMART').
        currency (str): The currency of the stock (e.g., 'USD').

    Returns:
        Dict[str, Any]: A dictionary containing:
            - 'connection_status': bool
            - 'account_summary': dict (mock or real)
            - 'market_data': dict (ticker data or error message)
            - 'error': str (optional, if major error occurs)
    """
    print(f"--- Initializing Stage One for account {account_code} ---")
    print(f"Attempting connection to {host}:{port} with client ID {client_id}")

    manager = ConnectionManager(host=host, port=port, client_id=client_id)
    results = {
        'connection_status': False,
        'account_summary': {},
        'market_data': None,
        'error': None
    }

    try:
        # 1. Connect and get IB instance
        ib_instance = manager.get_ib_instance()
        results['connection_status'] = manager.is_connected()
        print(f"Connection status: {results['connection_status']}")

        if not results['connection_status']:
            # get_ib_instance would raise ConnectionError if it fails.
            # This is an additional check, or if get_ib_instance is changed not to raise.
            results['error'] = "Failed to connect to Interactive Brokers."
            print(results['error'])
            # Attempt to get mock account summary even if connection failed
            results['account_summary'] = manager.get_account_summary(account_code=account_code)
            return results

        # 2. Get account summary
        print(f"Fetching account summary for {account_code}...")
        results['account_summary'] = manager.get_account_summary(account_code=account_code)
        print(f"Account summary: {results['account_summary']}")

        # 3. Fetch sample market data
        print(f"Fetching market data for {symbol} on {exchange}...")
        # Create a contract object
        # For US stocks, SMART is typical. For other instruments, details might vary.
        contract = Stock(symbol, exchange, currency)

        # It's good practice to qualify the contract if possible,
        # especially if there are multiple matches.
        # ib_instance.qualifyContracts(contract) # This can be time-consuming if not needed for simple ticker

        # Fetch ticker data
        # Ensure market data subscriptions are active if using live data.
        # For delayed data (if account doesn't have live subscriptions), set:
        # ib_instance.reqMarketDataType(4) # 1=live, 2=frozen, 3=delayed, 4=delayed frozen

        # For simplicity, let's try to get a snapshot.
        # If TWS/Gateway is not providing data (e.g. no market data permissions for symbol), this might hang or error.
        ticker = None
        try:
            ib_instance.reqMktData(contract, '', False, False)
            # Wait a bit for data to arrive - this is a common pattern with ib_insync
            # For a single snapshot, ib.ticker() might be simpler if it resolves quickly.
            # Or use reqTickByTickData for more granular data.
            # For robust applications, use event handlers.

            # Let's try to fetch the ticker after a short wait
            # This is a simplified approach. Production code would need more robust handling.
            ib_instance.sleep(2) # Wait for 2 seconds for data to arrive
            ticker = ib_instance.ticker(contract)

            if ticker and (ticker.last or ticker.close): # Check if some data is available
                results['market_data'] = {
                    'symbol': symbol,
                    'last_price': ticker.last,
                    'bid_price': ticker.bid,
                    'ask_price': ticker.ask,
                    'close_price': ticker.close,
                    'volume': ticker.volume,
                    'timestamp': ticker.time.isoformat() if ticker.time else None,
                }
                print(f"Market data for {symbol}: {results['market_data']}")
            else:
                results['market_data'] = f"No market data received for {symbol}. Ticker: {ticker}"
                print(results['market_data'])

        except Exception as md_e:
            results['market_data'] = f"Error fetching market data for {symbol}: {md_e}"
            print(results['market_data'])
        finally:
            # Clean up market data subscription
            if ib_instance.isConnected():
                ib_instance.cancelMktData(contract)


    except ConnectionError as ce:
        results['error'] = f"Stage One Connection Error: {ce}"
        print(results['error'])
        # Get mock summary if connection failed partway or was refused by manager
        results['account_summary'] = manager.get_account_summary(account_code=account_code)
        results['connection_status'] = False # Ensure this is false

    except Exception as e:
        results['error'] = f"An unexpected error occurred in Stage One: {e}"
        print(results['error'])
        # Attempt to get mock summary even in other errors
        if manager: # Check if manager was initialized
             results['account_summary'] = manager.get_account_summary(account_code=account_code)
        results['connection_status'] = manager.is_connected() if manager else False


    finally:
        if manager and manager.is_connected():
            print("Disconnecting at the end of Stage One.")
            manager.disconnect()
        else:
            print("No active connection to disconnect at the end of Stage One, or manager not initialized.")

        print("--- Stage One Initialization Complete ---")
        return results

if __name__ == '__main__':
    # Example Usage:
    # Ensure TWS or IB Gateway is running and accepting API connections
    # on 127.0.0.1:7497 (default for TWS) or 127.0.0.1:4002 (default for Gateway)

    # --- Test Case 1: Default connection (likely TWS Paper Trading) ---
    print("\n--- Running Stage One with default parameters (AAPL) ---")
    # Note: Real connection attempts will be made.
    # If TWS/Gateway is not running, this will result in a ConnectionError.
    stage_one_output_default = initialize_stage_one(port=7497, client_id=2) # Use a different client_id for testing
    print("\nStage One Output (Default - AAPL):")
    for key, value in stage_one_output_default.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for sub_key, sub_value in value.items():
                print(f"    {sub_key}: {sub_value}")
        else:
            print(f"  {key}: {value}")

    # --- Test Case 2: Using a different symbol, e.g., MSFT ---
    # print("\n\n--- Running Stage One for MSFT ---")
    # stage_one_output_msft = initialize_stage_one(symbol='MSFT', client_id=3)
    # print("\nStage One Output (MSFT):")
    # for key, value in stage_one_output_msft.items():
    #     if isinstance(value, dict):
    #         print(f"  {key}:")
    #         for sub_key, sub_value in value.items():
    #             print(f"    {sub_key}: {sub_value}")
    #     else:
    #         print(f"  {key}: {value}")

    # --- Test Case 3: Simulating connection failure (e.g., wrong port) ---
    # print("\n\n--- Running Stage One with invalid port (expect connection error) ---")
    # stage_one_output_fail = initialize_stage_one(port=9999, client_id=4) # Invalid port
    # print("\nStage One Output (Connection Fail):")
    # for key, value in stage_one_output_fail.items():
    #     if isinstance(value, dict):
    #         print(f"  {key}:")
    #         for sub_key, sub_value in value.items():
    #             print(f"    {sub_key}: {sub_value}")
    #     else:
    #         print(f"  {key}: {value}")
