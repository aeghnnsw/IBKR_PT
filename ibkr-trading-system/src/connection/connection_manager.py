from .ib_connector import IBConnector
from ib_insync import IB, AccountValue

class ConnectionManager:
    """
    Manages the connection to Interactive Brokers using IBConnector
    and provides access to connection details and basic account information.
    """
    _ib_connector: IBConnector | None = None
    _ib_instance: IB | None = None

    def __init__(self, host: str = '127.0.0.1', port: int = 7497, client_id: int = 1):
        """
        Initializes the ConnectionManager.

        Args:
            host (str): The host address of the TWS or IB Gateway.
            port (int): The port number for the TWS or IB Gateway.
            client_id (int): The client ID for the IB connection.
        """
        self.host = host
        self.port = port
        self.client_id = client_id
        # Ensure _ib_connector is initialized here if it's intended to be instance-specific
        # For a singleton-like connection, this might be handled differently.
        # For now, let's assume a new connector per ConnectionManager instance.
        self._ib_connector = IBConnector(host=self.host, port=self.port, client_id=self.client_id)

    def get_ib_instance(self) -> IB:
        """
        Establishes a connection if not already connected and returns the IB instance.

        Returns:
            IB: The connected ib_insync.IB instance.

        Raises:
            ConnectionError: If the connection cannot be established.
        """
        if self._ib_connector is None: # Should not happen with __init__ change
            self._ib_connector = IBConnector(host=self.host, port=self.port, client_id=self.client_id)

        if not self._ib_connector.is_connected():
            print("Attempting to connect via ConnectionManager...")
            try:
                self._ib_connector.connect()
                self._ib_instance = self._ib_connector.ib
            except ConnectionError as e:
                print(f"ConnectionManager failed to connect: {e}")
                # Propagate the error
                raise

        # Ensure _ib_instance is set if connector was already connected
        if self._ib_connector.is_connected() and self._ib_instance is None:
             self._ib_instance = self._ib_connector.ib

        if not self._ib_instance:
             # This case should ideally be prevented by the logic above
             raise ConnectionError("Failed to obtain IB instance from connector.")

        return self._ib_instance

    def disconnect(self):
        """
        Disconnects the current IB connection.
        """
        if self._ib_connector and self._ib_connector.is_connected():
            self._ib_connector.disconnect()
            self._ib_instance = None
        else:
            print("ConnectionManager: No active connection to disconnect.")

    def is_connected(self) -> bool:
        """
        Checks if the IB connection is currently active.

        Returns:
            bool: True if connected, False otherwise.
        """
        if self._ib_connector:
            return self._ib_connector.is_connected()
        return False

    def get_account_summary(self, account_code: str = "DU1234567") -> dict:
        """
        Fetches a summary of account values for the specified account or default.
        For now, this returns MOCK data if not connected, or if connection is real,
        attempts to fetch real data.

        Args:
            account_code (str): The account code to fetch summary for.
                                (Currently, this is a placeholder for future use with real data)

        Returns:
            dict: A dictionary containing account summary information.
                  Example: {'NetLiquidation': '100000', 'CashBalance': '50000'}
        """
        if not self.is_connected() or not self._ib_instance:
            print(f"ConnectionManager: Not connected. Returning mock account summary for {account_code}.")
            return {
                "AccountCode": account_code,
                "NetLiquidation": "1000000 (Mock)",
                "TotalCashValue": "1000000 (Mock)",
                "RealizedPnL": "0 (Mock)",
                "UnrealizedPnL": "0 (Mock)",
                "ConnectionStatus": "Disconnected - Mock Data"
            }

        try:
            # In a real scenario, you might want to qualify which account.
            # For now, let's try to get all account values and pick the first one if available
            # or look for a specific account if account_code was used to select one.
            # ib.accountValues() returns a list of AccountValue objects.
            # Each AccountValue has attributes: account, tag, value, currency.

            # This fetches all account values.
            acc_values = self._ib_instance.accountValues(account_code) # Pass account code if API supports filtering

            if not acc_values:
                print(f"ConnectionManager: No account values returned for {account_code}. Returning mock data.")
                return {"Error": "No account values returned", "AccountCode": account_code}

            summary = {"AccountCode": account_code, "ConnectionStatus": "Connected - Live Data"}
            # Filter for specific tags we are interested in
            for acc_val in acc_values:
                if acc_val.tag in ['NetLiquidation', 'TotalCashValue', 'RealizedPnL', 'UnrealizedPnL', 'CashBalance']:
                    summary[acc_val.tag] = acc_val.value

            # If a specific account_code was targeted, ensure we got data for it.
            # The current ib_insync behavior for accountValues(accountCode) might need checking.
            # If it still returns all accounts, one might need to filter:
            # specific_account_values = [av for av in acc_values if av.account == account_code]

            if len(summary) <= 2: # Only AccountCode and ConnectionStatus
                 print(f"ConnectionManager: Key financial tags not found for {account_code}. Returning what was found plus some mock as fallback.")
                 summary.update({
                    "NetLiquidation": summary.get("NetLiquidation", "N/A (Live-Check)"),
                    "TotalCashValue": summary.get("TotalCashValue", "N/A (Live-Check)"),
                    "Note": "Some values might be missing from live feed for this account."
                 })
            return summary

        except Exception as e:
            print(f"ConnectionManager: Error fetching account summary: {e}. Returning mock data.")
            return {
                "AccountCode": account_code,
                "Error": str(e),
                "NetLiquidation": "Error (Mock)",
                "TotalCashValue": "Error (Mock)",
                "ConnectionStatus": "Connected but error fetching - Mock Data"
            }

if __name__ == '__main__':
    # Example Usage (for testing purposes)
    manager = ConnectionManager() # Uses default host/port/client_id

    try:
        print("Attempting to connect via ConnectionManager...")
        ib = manager.get_ib_instance() # Establish connection
        print(f"Connection successful. IB instance: {ib}")
        print(f"Is connected: {manager.is_connected()}")

        print("\nFetching account summary (default account):")
        summary_default = manager.get_account_summary() # Uses default mock account for now if not connected
        for key, value in summary_default.items():
            print(f"  {key}: {value}")

        # Example for a specific account (still mock if not connected)
        # specific_account = "U123456"
        # print(f"\nFetching account summary for {specific_account}:")
        # summary_specific = manager.get_account_summary(account_code=specific_account)
        # for key, value in summary_specific.items():
        #     print(f"  {key}: {value}")

    except ConnectionError as ce:
        print(f"Main test block - Connection Error: {ce}")
    except Exception as e:
        print(f"Main test block - An unexpected error occurred: {e}")
    finally:
        if manager.is_connected():
            print("\nDisconnecting via ConnectionManager...")
            manager.disconnect()
            print(f"Is connected after disconnect: {manager.is_connected()}")
        else:
            # If connection failed, summary would be mock data
            print("\nFetching account summary (post-attempt, likely mock):")
            summary_default = manager.get_account_summary()
            for key, value in summary_default.items():
                print(f"  {key}: {value}")
            print("Was not connected, no disconnection performed by finally block.")
