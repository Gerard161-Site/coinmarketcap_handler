from typing import List, Optional, Dict, Any
from mindsdb.integrations.libs.api_handler_exceptions import MissingConnectionParams
from mindsdb.integrations.utilities.sql_utils import extract_comparison_conditions
from mindsdb_sql.parser.ast.select.constant import Constant
import pandas as pd


class CoinMarketCapTable:
    """Base class for CoinMarketCap tables."""
    
    def __init__(self, handler):
        self.handler = handler
    
    def get_columns(self) -> List[str]:
        """Return the list of columns for this table."""
        raise NotImplementedError()
    
    def select(self, query) -> pd.DataFrame:
        """Execute a SELECT query on this table."""
        raise NotImplementedError()


class CryptocurrencyQuotesTable(CoinMarketCapTable):
    """Table for cryptocurrency quotes/prices."""
    
    def get_columns(self) -> List[str]:
        return [
            'id', 'name', 'symbol', 'slug', 'cmc_rank', 'num_market_pairs',
            'circulating_supply', 'total_supply', 'max_supply', 'date_added',
            'platform', 'price', 'volume_24h', 'volume_change_24h',
            'percent_change_1h', 'percent_change_24h', 'percent_change_7d',
            'percent_change_30d', 'market_cap', 'market_cap_dominance',
            'fully_diluted_market_cap', 'last_updated'
        ]
    
    def select(self, query) -> pd.DataFrame:
        """Get cryptocurrency quotes."""
        conditions = extract_comparison_conditions(query.where)
        
        # Extract symbols if specified
        symbols = None
        symbol_condition = conditions.get('symbol')
        if symbol_condition and hasattr(symbol_condition[1], 'value'):
            symbols = symbol_condition[1].value
            if isinstance(symbols, str):
                symbols = [symbols]
        
        # Default to top cryptocurrencies if no symbol specified
        params = {}
        if symbols:
            params['symbol'] = ','.join(symbols)
        else:
            params['limit'] = 100  # Default limit
        
        # Get data from API
        response = self.handler.call_coinmarketcap_api('/v1/cryptocurrency/quotes/latest', params)
        
        if 'data' not in response:
            return pd.DataFrame(columns=self.get_columns())
        
        # Process response data
        rows = []
        data = response['data']
        
        # Handle both symbol-based and listing-based responses
        if isinstance(data, dict):
            # Symbol-based response
            for symbol, crypto_data in data.items():
                rows.append(self._process_crypto_data(crypto_data))
        elif isinstance(data, list):
            # Listing-based response
            for crypto_data in data:
                rows.append(self._process_crypto_data(crypto_data))
        
        return pd.DataFrame(rows, columns=self.get_columns())
    
    def _process_crypto_data(self, crypto_data: Dict) -> List:
        """Process individual cryptocurrency data."""
        quote = crypto_data.get('quote', {}).get('USD', {})
        platform = crypto_data.get('platform')
        
        return [
            crypto_data.get('id'),
            crypto_data.get('name'),
            crypto_data.get('symbol'),
            crypto_data.get('slug'),
            crypto_data.get('cmc_rank'),
            crypto_data.get('num_market_pairs'),
            crypto_data.get('circulating_supply'),
            crypto_data.get('total_supply'),
            crypto_data.get('max_supply'),
            crypto_data.get('date_added'),
            platform.get('name') if platform else None,
            quote.get('price'),
            quote.get('volume_24h'),
            quote.get('volume_change_24h'),
            quote.get('percent_change_1h'),
            quote.get('percent_change_24h'),
            quote.get('percent_change_7d'),
            quote.get('percent_change_30d'),
            quote.get('market_cap'),
            quote.get('market_cap_dominance'),
            quote.get('fully_diluted_market_cap'),
            quote.get('last_updated')
        ]


class CryptocurrencyListingsTable(CoinMarketCapTable):
    """Table for cryptocurrency listings."""
    
    def get_columns(self) -> List[str]:
        return [
            'id', 'name', 'symbol', 'slug', 'cmc_rank', 'num_market_pairs',
            'circulating_supply', 'total_supply', 'max_supply', 'date_added',
            'platform', 'price', 'volume_24h', 'percent_change_24h',
            'market_cap', 'last_updated'
        ]
    
    def select(self, query) -> pd.DataFrame:
        """Get cryptocurrency listings."""
        conditions = extract_comparison_conditions(query.where)
        
        # Set up parameters
        params = {
            'limit': 100,  # Default limit
            'convert': 'USD'
        }
        
        # Handle limit condition
        if hasattr(query, 'limit') and query.limit:
            params['limit'] = query.limit.value
        
        # Get data from API
        response = self.handler.call_coinmarketcap_api('/v1/cryptocurrency/listings/latest', params)
        
        if 'data' not in response:
            return pd.DataFrame(columns=self.get_columns())
        
        # Process response data
        rows = []
        for crypto_data in response['data']:
            quote = crypto_data.get('quote', {}).get('USD', {})
            platform = crypto_data.get('platform')
            
            rows.append([
                crypto_data.get('id'),
                crypto_data.get('name'),
                crypto_data.get('symbol'),
                crypto_data.get('slug'),
                crypto_data.get('cmc_rank'),
                crypto_data.get('num_market_pairs'),
                crypto_data.get('circulating_supply'),
                crypto_data.get('total_supply'),
                crypto_data.get('max_supply'),
                crypto_data.get('date_added'),
                platform.get('name') if platform else None,
                quote.get('price'),
                quote.get('volume_24h'),
                quote.get('percent_change_24h'),
                quote.get('market_cap'),
                quote.get('last_updated')
            ])
        
        return pd.DataFrame(rows, columns=self.get_columns())


class CryptocurrencyInfoTable(CoinMarketCapTable):
    """Table for cryptocurrency information."""
    
    def get_columns(self) -> List[str]:
        return [
            'id', 'name', 'symbol', 'category', 'description', 'slug',
            'logo', 'subreddit', 'notice', 'platform', 'date_added',
            'twitter_username', 'is_hidden', 'date_launched',
            'contract_address', 'self_reported_circulating_supply',
            'self_reported_market_cap', 'self_reported_tags'
        ]
    
    def select(self, query) -> pd.DataFrame:
        """Get cryptocurrency information."""
        conditions = extract_comparison_conditions(query.where)
        
        # Extract symbols if specified
        symbols = None
        symbol_condition = conditions.get('symbol')
        if symbol_condition and hasattr(symbol_condition[1], 'value'):
            symbols = symbol_condition[1].value
            if isinstance(symbols, str):
                symbols = [symbols]
        
        if not symbols:
            # Default to Bitcoin if no symbol specified
            symbols = ['BTC']
        
        params = {'symbol': ','.join(symbols)}
        
        # Get data from API
        response = self.handler.call_coinmarketcap_api('/v2/cryptocurrency/info', params)
        
        if 'data' not in response:
            return pd.DataFrame(columns=self.get_columns())
        
        # Process response data
        rows = []
        for symbol, crypto_data in response['data'].items():
            platform = crypto_data.get('platform')
            urls = crypto_data.get('urls', {})
            
            rows.append([
                crypto_data.get('id'),
                crypto_data.get('name'),
                crypto_data.get('symbol'),
                crypto_data.get('category'),
                crypto_data.get('description'),
                crypto_data.get('slug'),
                crypto_data.get('logo'),
                crypto_data.get('subreddit'),
                crypto_data.get('notice'),
                platform.get('name') if platform else None,
                crypto_data.get('date_added'),
                urls.get('twitter', [None])[0] if urls.get('twitter') else None,
                crypto_data.get('is_hidden'),
                crypto_data.get('date_launched'),
                platform.get('token_address') if platform else None,
                crypto_data.get('self_reported_circulating_supply'),
                crypto_data.get('self_reported_market_cap'),
                crypto_data.get('self_reported_tags')
            ])
        
        return pd.DataFrame(rows, columns=self.get_columns())


class GlobalMetricsTable(CoinMarketCapTable):
    """Table for global cryptocurrency metrics."""
    
    def get_columns(self) -> List[str]:
        return [
            'active_cryptocurrencies', 'total_cryptocurrencies', 'active_market_pairs',
            'active_exchanges', 'total_exchanges', 'eth_dominance', 'btc_dominance',
            'eth_dominance_yesterday', 'btc_dominance_yesterday', 'eth_dominance_24h_percentage_change',
            'btc_dominance_24h_percentage_change', 'defi_volume_24h', 'defi_volume_24h_reported',
            'defi_market_cap', '24h_volume_reported', 'altcoin_volume_24h',
            'altcoin_volume_24h_reported', 'altcoin_market_cap', 'total_market_cap',
            'total_volume_24h', 'total_volume_24h_reported', 'total_market_cap_yesterday',
            'total_volume_24h_yesterday', 'total_market_cap_percentage_change_24h',
            'total_volume_24h_percentage_change_24h', 'last_updated'
        ]
    
    def select(self, query) -> pd.DataFrame:
        """Get global cryptocurrency metrics."""
        # Get data from API
        response = self.handler.call_coinmarketcap_api('/v1/global-metrics/quotes/latest')
        
        if 'data' not in response:
            return pd.DataFrame(columns=self.get_columns())
        
        data = response['data']
        quote = data.get('quote', {}).get('USD', {})
        
        row = [
            data.get('active_cryptocurrencies'),
            data.get('total_cryptocurrencies'),
            data.get('active_market_pairs'),
            data.get('active_exchanges'),
            data.get('total_exchanges'),
            data.get('eth_dominance'),
            data.get('btc_dominance'),
            data.get('eth_dominance_yesterday'),
            data.get('btc_dominance_yesterday'),
            data.get('eth_dominance_24h_percentage_change'),
            data.get('btc_dominance_24h_percentage_change'),
            data.get('defi_volume_24h'),
            data.get('defi_volume_24h_reported'),
            data.get('defi_market_cap'),
            quote.get('total_volume_24h_reported'),
            data.get('altcoin_volume_24h'),
            data.get('altcoin_volume_24h_reported'),
            data.get('altcoin_market_cap'),
            quote.get('total_market_cap'),
            quote.get('total_volume_24h'),
            quote.get('total_volume_24h_reported'),
            data.get('total_market_cap_yesterday'),
            data.get('total_volume_24h_yesterday'),
            quote.get('total_market_cap_percentage_change_24h'),
            quote.get('total_volume_24h_percentage_change_24h'),
            data.get('last_updated')
        ]
        
        return pd.DataFrame([row], columns=self.get_columns())
