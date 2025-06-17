import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Adjust path to import from src
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if module_path not in sys.path:
    sys.path.append(module_path)

# Import the function to be tested
try:
    from stages import initialize_stage_one
    from connection.connection_manager import ConnectionManager # For type hinting or direct mock if needed
    from connection.ib_connector import IBConnector # For type hinting or direct mock if needed
except ImportError as e:
    print(f"Failed to import modules in test_stages.py: {e}")
    # This allows the file to be parsed, but tests will fail if imports are broken.
    initialize_stage_one = None
    ConnectionManager = None
    IBConnector = None


class TestInitializeStageOne(unittest.TestCase):

    @patch('stages.ConnectionManager') # Patch ConnectionManager where it's used in 'stages.py'
    def test_initialize_stage_one_success(self, MockConnectionManager):
        if initialize_stage_one is None:
            self.skipTest("Skipping test as initialize_stage_one could not be imported.")

        # Configure the mock ConnectionManager instance
        mock_manager_instance = MockConnectionManager.return_value
        mock_manager_instance.get_ib_instance.return_value = MagicMock() # Mocked IB instance
        mock_manager_instance.is_connected.return_value = True
        mock_manager_instance.get_account_summary.return_value = {
            'AccountCode': 'TestAcc123',
            'NetLiquidation': '100000 (Mock)',
            'ConnectionStatus': 'Connected - Mock Data for Test'
        }

        # Mock the IB instance methods (specifically for market data)
        mock_ib_instance = mock_manager_instance.get_ib_instance.return_value
        mock_ticker = MagicMock()
        mock_ticker.last = 150.0
        mock_ticker.bid = 149.9
        mock_ticker.ask = 150.1
        mock_ticker.close = 149.5
        mock_ticker.volume = 100000
        mock_ticker.time = MagicMock() # Mock the time attribute
        mock_ticker.time.isoformat.return_value = '2023-01-01T12:00:00' # Mock its isoformat method

        mock_ib_instance.ticker.return_value = mock_ticker
        mock_ib_instance.reqMktData = MagicMock()
        mock_ib_instance.cancelMktData = MagicMock()
        mock_ib_instance.sleep = MagicMock() # Mock ib_instance.sleep

        # Call the function
        results = initialize_stage_one(
            host='test_host',
            port=1234,
            client_id=99,
            account_code='TestAcc123',
            symbol='TEST',
            exchange='TESTEX',
            currency='TSD'
        )

        # Assertions
        self.assertTrue(results['connection_status'])
        self.assertEqual(results['account_summary']['AccountCode'], 'TestAcc123')
        self.assertIn('NetLiquidation', results['account_summary'])
        self.assertIsNotNone(results['market_data'])
        self.assertEqual(results['market_data']['symbol'], 'TEST')
        self.assertEqual(results['market_data']['last_price'], 150.0)
        self.assertIsNone(results['error'])

        # Verify that ConnectionManager was called with correct parameters
        MockConnectionManager.assert_called_once_with(host='test_host', port=1234, client_id=99)

        # Verify IB instance methods were called
        mock_manager_instance.get_ib_instance.assert_called_once()
        mock_manager_instance.get_account_summary.assert_called_once_with(account_code='TestAcc123')
        mock_ib_instance.reqMktData.assert_called_once()
        # args, kwargs = mock_ib_instance.reqMktData.call_args
        # self.assertEqual(args[0].symbol, 'TEST') # Check contract details
        mock_ib_instance.cancelMktData.assert_called_once()
        mock_manager_instance.disconnect.assert_called_once()


    @patch('stages.ConnectionManager')
    def test_initialize_stage_one_connection_failure(self, MockConnectionManager):
        if initialize_stage_one is None:
            self.skipTest("Skipping test as initialize_stage_one could not be imported.")

        # Configure the mock ConnectionManager to simulate connection failure
        mock_manager_instance = MockConnectionManager.return_value
        # Simulate ConnectionError being raised by get_ib_instance
        mock_manager_instance.get_ib_instance.side_effect = ConnectionError("Test connection failed")

        # Mock other methods that might be called even if connection fails (e.g. get_account_summary for mock data)
        mock_manager_instance.is_connected.return_value = False # Should reflect no connection
        mock_manager_instance.get_account_summary.return_value = {
            'AccountCode': 'TestAccFail',
            'NetLiquidation': 'Error (Mock)',
            'ConnectionStatus': 'Disconnected - Mock Data'
        }

        # Call the function
        results = initialize_stage_one(
            host='fail_host',
            port=5678,
            client_id=100,
            account_code='TestAccFail'
        )

        # Assertions
        self.assertFalse(results['connection_status'])
        self.assertIsNotNone(results['error'])
        self.assertIn("Test connection failed", results['error'])
        self.assertEqual(results['account_summary']['AccountCode'], 'TestAccFail')
        self.assertIn('NetLiquidation', results['account_summary']) # Should get mock summary
        self.assertIsNone(results['market_data']) # No market data if connection fails

        # Verify ConnectionManager was called
        MockConnectionManager.assert_called_once_with(host='fail_host', port=5678, client_id=100)
        mock_manager_instance.get_ib_instance.assert_called_once()
        # Ensure disconnect is not called if never connected, or called if manager tracks connection state internally for cleanup
        # Based on current initialize_stage_one, disconnect might be called in finally if manager exists
        # If manager.is_connected() is false, it prints "No active connection to disconnect..."
        # So, checking manager.disconnect() call is still valid.
        mock_manager_instance.disconnect.assert_called_once()


    @patch('stages.ConnectionManager')
    def test_initialize_stage_one_market_data_failure(self, MockConnectionManager):
        if initialize_stage_one is None:
            self.skipTest("Skipping test as initialize_stage_one could not be imported.")

        mock_manager_instance = MockConnectionManager.return_value
        mock_manager_instance.get_ib_instance.return_value = MagicMock()
        mock_manager_instance.is_connected.return_value = True
        mock_manager_instance.get_account_summary.return_value = {'AccountCode': 'TestMDfail', 'NetLiquidation': 'OK'}

        mock_ib_instance = mock_manager_instance.get_ib_instance.return_value
        mock_ib_instance.reqMktData = MagicMock()
        mock_ib_instance.ticker.return_value = None # Simulate no ticker data returned
        mock_ib_instance.sleep = MagicMock()
        mock_ib_instance.cancelMktData = MagicMock()

        results = initialize_stage_one(symbol='NOSTOCK')

        self.assertTrue(results['connection_status'])
        self.assertIsNotNone(results['account_summary'])
        self.assertTrue(isinstance(results['market_data'], str)) # Expecting an error string
        self.assertIn("No market data received for NOSTOCK", results['market_data'])
        self.assertIsNone(results['error']) # No top-level error

        mock_ib_instance.reqMktData.assert_called_once()
        mock_ib_instance.cancelMktData.assert_called_once()
        mock_manager_instance.disconnect.assert_called_once()

if __name__ == '__main__':
    # Ensure the script can be run directly for testing, e.g. from the tests directory
    # This setup helps if you run `python test_stages.py`
    # For running with `python -m unittest discover`, the path adjustment at the top is key.
    unittest.main()
