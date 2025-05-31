connection_args = {
    'api_key': {
        'type': 'str',
        'description': 'CoinMarketCap API key'
    },
    'sandbox': {
        'type': 'bool',
        'description': 'Use sandbox API',
        'default': False
    }
}
connection_args_example = {
    'api_key': 'your_api_key_here',
    'sandbox': True
}