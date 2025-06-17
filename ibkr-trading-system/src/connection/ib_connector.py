from ib_insync import IB, ConnectionStats

class IBConnector:
    """
    Handles the connection to Interactive Brokers (IB) using the ib_insync library.
    """
    def __init__(self, host: str = '127.0.0.1', port: int = 7497, client_id: int = 1):
        """
        Initializes the IBConnector.

        Args:
            host (str): The host address of the TWS or IB Gateway.
            port (int): The port number for the TWS or IB Gateway.
            client_id (int): The client ID for the IB connection.
        """
        self.ib = IB()
        self.host = host
        self.port = port
        self.client_id = client_id
        self._is_connected = False

    def connect(self):
        """
        Connects to Interactive Brokers.
        Raises:
            ConnectionError: If the connection fails.
        """
        if not self.ib.isConnected():
            try:
                self.ib.connect(self.host, self.port, self.client_id)
                self._is_connected = True
                print(f"Successfully connected to IB: {self.host}:{self.port} with client ID {self.client_id}")
            except ConnectionRefusedError:
                self._is_connected = False
                print(f"Connection refused. Ensure TWS or IB Gateway is running and API connections are enabled on {self.host}:{self.port}.")
                raise ConnectionError(f"Connection refused by IB Gateway/TWS on {self.host}:{self.port}")
            except Exception as e:
                self._is_connected = False
                print(f"An error occurred during connection: {e}")
                raise ConnectionError(f"Failed to connect to IB: {e}")
        else:
            self._is_connected = True
            print("Already connected to IB.")

    def disconnect(self):
        """
        Disconnects from Interactive Brokers.
        """
        if self.ib.isConnected():
            self.ib.disconnect()
            self._is_connected = False
            print("Successfully disconnected from IB.")
        else:
            print("Not connected to IB, no need to disconnect.")

    def is_connected(self) -> bool:
        """
        Checks the current connection status.

        Returns:
            bool: True if connected, False otherwise.
        """
        # Update internal status based on ib_insync's check,
        # as connection can be lost externally
        if self.ib.isConnected():
            self._is_connected = True
        else:
            self._is_connected = False
        return self._is_connected

    def connection_stats(self) -> ConnectionStats | None:
        """
        Retrieves connection statistics if connected.

        Returns:
            ConnectionStats | None: Connection statistics object or None if not connected.
        """
        if self.is_connected():
            return self.ib.connectionStats
        return None

if __name__ == '__main__':
    # Example Usage (for testing purposes)
    connector = IBConnector()
    try:
        print(f"Attempting to connect to TWS/Gateway on {connector.host}:{connector.port}...")
        connector.connect()
        print(f"Connection status: {connector.is_connected()}")

        if connector.is_connected():
            stats = connector.connection_stats()
            if stats:
                print(f"Connection Stats: {stats}")

    except ConnectionError as ce:
        print(f"Connection Error: {ce}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if connector.is_connected():
            print("Disconnecting...")
            connector.disconnect()
            print(f"Connection status after disconnect: {connector.is_connected()}")
        else:
            print("Was not connected, no disconnection needed.")
