"""
CoinMarketCap API Tables for MindsDB Handler
"""

import pandas as pd
from typing import List, Dict, Any, Optional
from mindsdb_sql import parse_sql
from mindsdb.integrations.libs.api_handler_exceptions import APIHandlerException


class QuotesTable:
    """Table for cryptocurrency quotes/prices"""
    
    def __init__(self, handler):
        self.handler = handler
    
    def select(self, query) -> pd.DataFrame:
        """
        Handle SELECT queries for cryptocurrency quotes
        """
        try:
            # Parse conditions from the query
            conditions = self._parse_conditions(query.where)
            
            # Extract symbols if specified
            symbols = self._extract_symbols(conditions)
            
            # Get limit if specified
            limit = getattr(query, 'limit', None)
            if limit:
                limit = limit.value if hasattr(limit, 'value') else limit
            
            # Make API request
            data = self._fetch_quotes_data(symbols=symbols, limit=limit)
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            return df
            
        except Exception as e:
            raise APIHandlerException(f"Error querying quotes table: {str(e)}")
    
    def _parse_conditions(self, where_clause) -> Dict[str, Any]:
        """Parse WHERE conditions from query"""
        conditions = {}
        
        if not where_clause:
            return conditions
            
        # Handle different condition formats
        if hasattr(where_clause, 'args'):
            # Handle multiple conditions (AND/OR)
            for condition in where_clause.args:
                self._extract_condition(condition, conditions)
        else:
            # Handle single condition
            self._extract_condition(where_clause, conditions)
            
        return conditions
    
    def _extract_condition(self, condition, conditions: Dict[str, Any]):
        """Extract a single condition"""
        if hasattr(condition, 'left') and hasattr(condition, 'right'):
            column = str(condition.left).lower()
            value = condition.right
            
            # Handle different value types
            if hasattr(value, 'value'):
                value = value.value
            elif hasattr(value, 'args'):
                # Handle IN clauses
                value = [arg.value if hasattr(arg, 'value') else str(arg) for arg in value.args]
            
            conditions[column] = value
    
    def _extract_symbols(self, conditions: Dict[str, Any]) -> Optional[List[str]]:
        """Extract cryptocurrency symbols from conditions"""
        symbols = None
        
        if 'symbol' in conditions:
            symbol_value = conditions['symbol']
            if isinstance(symbol_value, str):
                symbols = [symbol_value.upper()]
            elif isinstance(symbol_value, list):
                symbols = [s.upper() if isinstance(s, str) else str(s).upper() for s in symbol_value]
        
        return symbols
    
    def _fetch_quotes_data(self, symbols: Optional[List[str]] = None, limit: Optional[int] = None) -> List[Dict]:
        """Fetch quotes data from CoinMarketCap API"""
        try:
            if symbols:
                # Get specific cryptocurrencies
                data = self.handler.api_client.get_quotes(symbols=symbols)
            else:
                # Get latest listings
                limit = limit or 100  # Default limit
                data = self.handler.api_client.get_listings(limit=limit)
            
            return data
            
        except Exception as e:
            raise APIHandlerException(f"Error fetching quotes data: {str(e)}")


class ListingsTable:
    """Table for cryptocurrency listings"""
    
    def __init__(self, handler):
        self.handler = handler
    
    def select(self, query) -> pd.DataFrame:
        """Handle SELECT queries for cryptocurrency listings"""
        try:
            # Get limit if specified
            limit = getattr(query, 'limit', None)
            if limit:
                limit = limit.value if hasattr(limit, 'value') else limit
            else:
                limit = 100  # Default limit
            
            # Make API request
            data = self.handler.api_client.get_listings(limit=limit)
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            return df
            
        except Exception as e:
            raise APIHandlerException(f"Error querying listings table: {str(e)}")


class InfoTable:
    """Table for cryptocurrency information"""
    
    def __init__(self, handler):
        self.handler = handler
    
    def select(self, query) -> pd.DataFrame:
        """Handle SELECT queries for cryptocurrency info"""
        try:
            # Parse conditions
            conditions = self._parse_conditions(query.where)
            
            # Extract symbols
            symbols = self._extract_symbols(conditions)
            
            if not symbols:
                raise APIHandlerException("Symbol parameter is required for info table")
            
            # Make API request
            data = self.handler.api_client.get_info(symbols=symbols)
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            return df
            
        except Exception as e:
            raise APIHandlerException(f"Error querying info table: {str(e)}")
    
    def _parse_conditions(self, where_clause) -> Dict[str, Any]:
        """Parse WHERE conditions from query"""
        conditions = {}
        
        if not where_clause:
            return conditions
            
        # Handle different condition formats
        if hasattr(where_clause, 'args'):
            # Handle multiple conditions (AND/OR)
            for condition in where_clause.args:
                self._extract_condition(condition, conditions)
        else:
            # Handle single condition
            self._extract_condition(where_clause, conditions)
            
        return conditions
    
    def _extract_condition(self, condition, conditions: Dict[str, Any]):
        """Extract a single condition"""
        if hasattr(condition, 'left') and hasattr(condition, 'right'):
            column = str(condition.left).lower()
            value = condition.right
            
            # Handle different value types
            if hasattr(value, 'value'):
                value = value.value
            elif hasattr(value, 'args'):
                # Handle IN clauses
                value = [arg.value if hasattr(arg, 'value') else str(arg) for arg in value.args]
            
            conditions[column] = value
    
    def _extract_symbols(self, conditions: Dict[str, Any]) -> Optional[List[str]]:
        """Extract cryptocurrency symbols from conditions"""
        symbols = None
        
        if 'symbol' in conditions:
            symbol_value = conditions['symbol']
            if isinstance(symbol_value, str):
                symbols = [symbol_value.upper()]
            elif isinstance(symbol_value, list):
                symbols = [s.upper() if isinstance(s, str) else str(s).upper() for s in symbol_value]
        
        return symbols


class GlobalMetricsTable:
    """Table for global cryptocurrency metrics"""
    
    def __init__(self, handler):
        self.handler = handler
    
    def select(self, query) -> pd.DataFrame:
        """Handle SELECT queries for global metrics"""
        try:
            # Make API request
            data = self.handler.api_client.get_global_metrics()
            
            # Convert to DataFrame (single row)
            df = pd.DataFrame([data])
            
            return df
            
        except Exception as e:
            raise APIHandlerException(f"Error querying global metrics table: {str(e)}") 