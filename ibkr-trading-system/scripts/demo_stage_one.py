import sys
import os
import json # For pretty printing dicts, though manual printing is also fine

# Adjust path to include the 'src' directory
# This assumes the script is in 'scripts/' and 'src/' is a sibling of 'scripts/'
# ../src
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if module_path not in sys.path:
    sys.path.append(module_path)

try:
    from stages import initialize_stage_one
except ImportError as e:
    print(f"Error importing initialize_stage_one: {e}")
    print(f"Current sys.path: {sys.path}")
    print("Please ensure 'ibkr-trading-system/src' is in your Python path or the script is run from the project root.")
    sys.exit(1) # Exit if the core function cannot be imported

def run_stage_one_demo():
    """
    Runs the Stage One initialization demo.
    """
    print("--- Stage One Initialization Demo Script ---")
    print("This script demonstrates the `initialize_stage_one` function.")
    print("It will attempt to connect to Interactive Brokers, fetch account summary,")
    print("and retrieve sample market data.")
    print("\n**Important:** Ensure TWS or IB Gateway is running, logged in, and")
    print("configured for API connections on the specified host and port.")
    print("-" * 50)

    # Connection parameters - MODIFY THESE IF YOUR SETUP IS DIFFERENT
    IB_HOST = '127.0.0.1'
    IB_PORT = 7497  # Default for TWS Paper trading. Use 4002 for IB Gateway Paper trading.
    CLIENT_ID = 102 # Choose a unique client ID, different from notebook if run concurrently
    ACCOUNT_CODE = 'DU1234567' # Replace with your paper trading account for more accurate testing
    STOCK_SYMBOL = 'AAPL'
    STOCK_EXCHANGE = 'SMART'
    STOCK_CURRENCY = 'USD'

    print("\nUsing the following parameters:")
    print(f"  Host: {IB_HOST}")
    print(f"  Port: {IB_PORT}")
    print(f"  Client ID: {CLIENT_ID}")
    print(f"  Account Code: {ACCOUNT_CODE}")
    print(f"  Symbol: {STOCK_SYMBOL} on {STOCK_EXCHANGE} ({STOCK_CURRENCY})")
    print("-" * 50)

    stage_one_results = None
    try:
        stage_one_results = initialize_stage_one(
            host=IB_HOST,
            port=IB_PORT,
            client_id=CLIENT_ID,
            account_code=ACCOUNT_CODE,
            symbol=STOCK_SYMBOL,
            exchange=STOCK_EXCHANGE,
            currency=STOCK_CURRENCY
        )
    except Exception as e:
        print(f"\nAn unexpected error occurred while running initialize_stage_one: {e}")
        print("This might be due to issues with the IB connection or the function itself.")
        print("-" * 50)
        # No need to return here, results will be None and handled below

    if stage_one_results:
        print("\n--- Stage One Results ---")
        print(f"Connection Status: {stage_one_results.get('connection_status')}")

        print("\nAccount Summary:")
        account_summary = stage_one_results.get('account_summary', {})
        if isinstance(account_summary, dict) and account_summary:
            for key, value in account_summary.items():
                print(f"  {key}: {value}")
        elif account_summary: # if it's a string or other non-empty non-dict
             print(f"  {account_summary}")
        else:
            print("  No account summary data returned.")

        print("\nMarket Data:")
        market_data = stage_one_results.get('market_data')
        if isinstance(market_data, dict) and market_data:
            for key, value in market_data.items():
                print(f"  {key}: {value}")
        elif market_data: # Handles cases where it's an error string or other non-empty non-dict
            print(f"  {market_data}")
        else:
            print("  No market data returned.")

        if stage_one_results.get('error'):
            print(f"\nError during Stage One: {stage_one_results.get('error')}")
    else:
        print("\nStage one results are not available. A significant error likely occurred during execution.")

    print("-" * 50)
    print("Demo script finished.")

if __name__ == '__main__':
    run_stage_one_demo()
