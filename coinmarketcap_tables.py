from typing import List, Optional, Dict, Any
from mindsdb.integrations.libs.api_handler import APITable
from mindsdb.integrations.utilities.sql_utils import extract_comparison_conditions
from mindsdb_sql_parser.ast import Constant
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


class CryptocurrencyQuotesTable(APITable):
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
        
        # Fix conditions processing - it returns a list of tuples
        symbols = None
        for op, arg1, arg2 in conditions:
            if arg1 == 'symbol':
                if op == '=':
                    symbols = [arg2] if isinstance(arg2, str) else arg2
                elif op == 'IN':
                    symbols = arg2 if isinstance(arg2, list) else [arg2]
        
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


class CryptocurrencyListingsTable(APITable):
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
        
        # Fix conditions processing
        for op, arg1, arg2 in conditions:
            if arg1 == 'limit' and op == '=':
                params['limit'] = arg2
        
        # Handle limit from query object
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


class CryptocurrencyInfoTable(APITable):
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
        
        # Fix conditions processing
        symbols = None
        for op, arg1, arg2 in conditions:
            if arg1 == 'symbol':
                if op == '=':
                    symbols = [arg2] if isinstance(arg2, str) else arg2
                elif op == 'IN':
                    symbols = arg2 if isinstance(arg2, list) else [arg2]
        
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
                crypto_data.get('twitter_username'),
                crypto_data.get('is_hidden'),
                crypto_data.get('date_launched'),
                platform.get('token_address') if platform else None,
                crypto_data.get('self_reported_circulating_supply'),
                crypto_data.get('self_reported_market_cap'),
                crypto_data.get('self_reported_tags')
            ])
        
        return pd.DataFrame(rows, columns=self.get_columns())


class GlobalMetricsTable(APITable):
    """Table for global cryptocurrency market metrics."""
    
    def get_columns(self) -> List[str]:
        return [
            'active_cryptocurrencies', 'total_cryptocurrencies', 'active_market_pairs',
            'active_exchanges', 'total_exchanges', 'eth_dominance', 'btc_dominance',
            'total_market_cap', 'total_volume_24h', 'total_volume_24h_reported',
            'altcoin_volume_24h', 'altcoin_market_cap', 'defi_volume_24h',
            'defi_volume_24h_reported', 'defi_market_cap', 'stablecoin_volume_24h',
            'stablecoin_volume_24h_reported', 'stablecoin_market_cap',
            'derivatives_volume_24h', 'derivatives_volume_24h_reported',
            'quote_last_updated'
        ]
    
    def select(self, query) -> pd.DataFrame:
        """Get global market metrics."""
        # No specific conditions needed for global metrics
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
            quote.get('total_market_cap'),
            quote.get('total_volume_24h'),
            quote.get('total_volume_24h_reported'),
            quote.get('altcoin_volume_24h'),
            quote.get('altcoin_market_cap'),
            quote.get('defi_volume_24h'),
            quote.get('defi_volume_24h_reported'),
            quote.get('defi_market_cap'),
            quote.get('stablecoin_volume_24h'),
            quote.get('stablecoin_volume_24h_reported'),
            quote.get('stablecoin_market_cap'),
            quote.get('derivatives_volume_24h'),
            quote.get('derivatives_volume_24h_reported'),
            quote.get('last_updated')
        ]
        
        return pd.DataFrame([row], columns=self.get_columns())
