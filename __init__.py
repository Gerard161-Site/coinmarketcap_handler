import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Loading CoinMarketCap handler")

from .__about__ import __version__ as version, __description__ as description
from .connection_args import connection_args, connection_args_example

try:
    from .coinmarketcap_handler import CoinMarketCapHandler as Handler
    import_error = None
    logger.debug("Successfully imported CoinMarketCapHandler")
except Exception as e:
    Handler = None
    import_error = e
    logger.error(f"Failed to import CoinMarketCapHandler: {e}")

title = 'CoinMarketCap'
name = 'coinmarketcap'
type = 'data'  # Changed from HANDLER_TYPE.DATA
icon_path = 'icon.svg'

__all__ = [
    'Handler', 'version', 'name', 'type', 'title', 'description',
    'connection_args', 'connection_args_example', 'import_error', 'icon_path'
]