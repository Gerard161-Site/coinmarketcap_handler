from mindsdb.integrations.libs.const import HANDLER_TYPE

from .__about__ import __version__ as version, __description__ as description
from .connection_args import connection_args, connection_args_example

try:
    from .coinmarketcap_handler import CoinMarketCapHandler as Handler
    import_error = None
except Exception as e:
    Handler = None
    import_error = e

title = "CoinMarketCap"
name = "coinmarketcap"
type = HANDLER_TYPE.DATA
icon_path = "icon.svg"

__all__ = [
    "Handler", "version", "name", "type", "title", "description",
    "connection_args", "connection_args_example", "import_error", "icon_path"
]