import unittest
import pandas as pd
from unittest.mock import Mock, patch
from coinmarketcap_handler.coinmarketcap_handler import CoinMarketCapHandler
from coinmarketcap_handler.coinmarketcap_tables import CryptocurrencyQuotesTable


class TestCoinMarketCapHandler(unittest.TestCase):
    """Test cases for CoinMarketCap handler."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.handler = CoinMarketCapHandler(
            'test_coinmarketcap',
            connection_data={
                'api_key': 'test_api_key',
                'sandbox': True
            }
        )
    
    def test_handler_initialization(self):
        """Test handler initialization."""
        self.assertEqual(self.handler.name, 'coinmarketcap')
        self.assertEqual(self.handler.api_key, 'test_api_key')
        self.assertTrue(self.handler.is_sandbox)
        self.assertIn('quotes', self.handler._tables)
        self.assertIn('listings', self.handler._tables)
        self.assertIn('info', self.handler._tables)
        self.assertIn('global_metrics', self.handler._tables)
    
    @patch('requests.get')
    def test_successful_connection(self, mock_get):
        """Test successful API connection."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = {
            'status': {'error_code': 0},
            'data': {}
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.handler.connect()
        self.assertTrue(result.success)
        self.assertTrue(self.handler.is_connected)
    
    @patch('requests.get')
    def test_failed_connection(self, mock_get):
        """Test failed API connection."""
        # Mock failed API response
        mock_response = Mock()
        mock_response.json.return_value = {
            'status': {
                'error_code': 1001,
                'error_message': 'API key invalid'
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.handler.connect()
        self.assertFalse(result.success)
        self.assertFalse(self.handler.is_connected)
        self.assertIn('API key invalid', result.error_message)
    
    @patch('requests.get')
    def test_quotes_table_select(self, mock_get):
        """Test quotes table select operation."""
        # Mock API response for quotes
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': {
                'BTC': {
                    'id': 1,
                    'name': 'Bitcoin',
                    'symbol': 'BTC',
                    'slug': 'bitcoin',
                    'cmc_rank': 1,
                    'quote': {
                        'USD': {
                            'price': 50000.0,
                            'volume_24h': 30000000000,
                            'percent_change_24h': 2.5,
                            'market_cap': 950000000000
                        }
                    }
                }
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        quotes_table = CryptocurrencyQuotesTable(self.handler)
        
        # Mock query object
        mock_query = Mock()
        mock_query.where = None
        
        result = quotes_table.select(mock_query)
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]['symbol'], 'BTC')
        self.assertEqual(result.iloc[0]['price'], 50000.0)
    
    def test_get_columns(self):
        """Test get_columns method for quotes table."""
        quotes_table = CryptocurrencyQuotesTable(self.handler)
        columns = quotes_table.get_columns()
        
        expected_columns = [
            'id', 'name', 'symbol', 'slug', 'cmc_rank', 'price',
            'volume_24h', 'percent_change_24h', 'market_cap'
        ]
        
        for col in expected_columns:
            self.assertIn(col, columns)


if __name__ == '__main__':
    unittest.main()