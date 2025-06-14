
import requests
from typing import Optional, Dict, Any
from mindsdb.integrations.libs.api_handler import APIHandler
from mindsdb.integrations.libs.response import (
    HandlerStatusResponse as StatusResponse,
    HandlerResponse as Response,
    RESPONSE_TYPE
)
from mindsdb.utilities import log
from mindsdb_sql_parser import parse_sql
from .coinmarketcap_tables import (
    CryptocurrencyQuotesTable,
    CryptocurrencyListingsTable,
    CryptocurrencyInfoTable,
    GlobalMetricsTable
)

logger = log.getLogger(__name__)


class CoinMarketCapHandler(APIHandler):
    """
    The CoinMarketCap handler implementation.
    """
    
    name = 'coinmarketcap'
    
    def __init__(self, name: str, **kwargs):
        """
        Initialize the CoinMarketCap handler.
        
        Args:
            name (str): The handler name
            kwargs: Connection arguments including api_key
        """
        super().__init__(name)
        
        # Connection parameters
        connection_data = kwargs.get('connection_data', {})
        self.api_key = connection_data.get('api_key')
        self.is_sandbox = connection_data.get('sandbox', False)
        
        # API configuration
        self.base_url = 'https://sandbox-api.coinmarketcap.com' if self.is_sandbox else 'https://pro-api.coinmarketcap.com'
        self.headers = {
            'Accepts': 'application/json',
            'Accept-Encoding': 'deflate, gzip'
        }
        
        if self.api_key:
            self.headers['X-CMC_PRO_API_KEY'] = self.api_key
        
        # Register available tables
        self._register_table('quotes', CryptocurrencyQuotesTable(self))
        self._register_table('listings', CryptocurrencyListingsTable(self))
        self._register_table('info', CryptocurrencyInfoTable(self))
        self._register_table('global_metrics', GlobalMetricsTable(self))
        
    def connect(self) -> StatusResponse:
        """
        Set up any connections required by the handler.
        
        Returns:
            HandlerStatusResponse
        """
        try:
            # Test connection by making a simple API call
            response = self.call_coinmarketcap_api('/v1/global-metrics/quotes/latest')
            if response.get('status', {}).get('error_code') == 0:
                self.is_connected = True
                return StatusResponse(True)
            else:
                self.is_connected = False
                error_msg = response.get('status', {}).get('error_message', 'Unknown error')
                return StatusResponse(False, f"Connection failed: {error_msg}")
        except Exception as e:
            self.is_connected = False
            logger.error(f"Error connecting to CoinMarketCap: {e}")
            return StatusResponse(False, f"Connection failed: {str(e)}")
    
    def check_connection(self) -> StatusResponse:
        """
        Check if the connection is alive and healthy.
        
        Returns:
            HandlerStatusResponse
        """
        return self.connect()
    
    def native_query(self, query: str) -> Response:
        """
        Receive and process a raw query.
        
        Args:
            query (str): query in native format
            
        Returns:
            HandlerResponse
        """
        ast = parse_sql(query, dialect='mindsdb')
        return self.query(ast)
    
    def call_coinmarketcap_api(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Call CoinMarketCap API endpoint.
        
        Args:
            endpoint (str): API endpoint path
            params (dict): Optional query parameters
            
        Returns:
            dict: API response data
        """
        url = self.base_url + endpoint
        
        try:
            response = requests.get(url, headers=self.headers, params=params or {})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in API call: {e}")
            raise
