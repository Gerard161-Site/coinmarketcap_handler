# CoinMarketCap Handler for MindsDB

This handler integrates MindsDB with the CoinMarketCap API, enabling you to access real-time cryptocurrency market data, prices, and metrics directly from your MindsDB instance.

## Overview

The CoinMarketCap handler allows you to:
- Get real-time cryptocurrency prices and market data
- Access cryptocurrency listings and rankings  
- Retrieve detailed cryptocurrency information
- Monitor global cryptocurrency market metrics
- Use cryptocurrency data for ML predictions and analysis

## Prerequisites

Before proceeding, ensure the following prerequisites are met:

- Install MindsDB locally via [Docker](https://docs.mindsdb.com/setup/self-hosted/docker) or [Docker Desktop](https://docs.mindsdb.com/setup/self-hosted/docker-desktop)
- A CoinMarketCap API key (get it from [CoinMarketCap Developer Portal](https://coinmarketcap.com/api/))

## Installation

### Option 1: Install from GitHub (Recommended for Development)

1. Clone this repository:
```bash
git clone https://github.com/your-username/mindsdb-coinmarketcap-handler.git
cd mindsdb-coinmarketcap-handler
```

2. Install the handler:
```bash
pip install -e .
```

3. Copy the handler to your MindsDB installation:
```bash
# If you have MindsDB installed from source
cp -r coinmarketcap_handler /path/to/mindsdb/mindsdb/integrations/handlers/

# If you have MindsDB installed via pip
cp -r coinmarketcap_handler /path/to/site-packages/mindsdb/integrations/handlers/
```

### Option 2: Direct Installation in MindsDB

1. Navigate to your MindsDB handlers directory:
```bash
cd /path/to/mindsdb/mindsdb/integrations/handlers/
```

2. Clone this repository:
```bash
git clone https://github.com/your-username/mindsdb-coinmarketcap-handler.git coinmarketcap_handler
```

3. Install dependencies:
```bash
cd coinmarketcap_handler
pip install -r requirements.txt
```

### Option 3: Docker Installation

If you're using MindsDB with Docker, you can create a custom image:

```dockerfile
FROM mindsdb/mindsdb:latest

# Copy the handler
COPY coinmarketcap_handler /opt/mindsdb/mindsdb/integrations/handlers/coinmarketcap_handler/

# Install dependencies
RUN pip install requests>=2.25.0 pandas>=1.3.0

EXPOSE 47334 47335
```

Build and run:
```bash
docker build -t mindsdb-with-coinmarketcap .
docker run -p 47334:47334 -p 47335:47335 mindsdb-with-coinmarketcap
```

## Connection

This handler is implemented using the CoinMarketCap API and requires an API key for authentication.

### Getting Your API Key

1. Go to [CoinMarketCap Developer Portal](https://coinmarketcap.com/api/)
2. Sign up for a free account
3. Navigate to your API dashboard
4. Copy your API key

### Connecting to MindsDB

To connect CoinMarketCap to MindsDB, use the following SQL command:

```sql
CREATE DATABASE my_coinmarketcap
WITH ENGINE = 'coinmarketcap',
PARAMETERS = {
    "api_key": "your_coinmarketcap_api_key_here"
};
```

For testing purposes, you can use the sandbox environment:

```sql
CREATE DATABASE my_coinmarketcap_sandbox
WITH ENGINE = 'coinmarketcap',
PARAMETERS = {
    "api_key": "your_coinmarketcap_api_key_here",
    "sandbox": true
};
```

## Usage

The CoinMarketCap handler provides access to several data tables:

### 1. Cryptocurrency Quotes (`quotes`)

Get real-time cryptocurrency prices and market data:

```sql
-- Get Bitcoin price data
SELECT * FROM my_coinmarketcap.quotes WHERE symbol = 'BTC';

-- Get multiple cryptocurrencies
SELECT symbol, name, price, market_cap, percent_change_24h 
FROM my_coinmarketcap.quotes 
WHERE symbol IN ('BTC', 'ETH', 'ADA');

-- Get top 50 cryptocurrencies by market cap
SELECT symbol, name, price, market_cap, cmc_rank
FROM my_coinmarketcap.quotes 
ORDER BY cmc_rank 
LIMIT 50;
```

### 2. Cryptocurrency Listings (`listings`)

Get cryptocurrency listings with ranking information:

```sql
-- Get top 100 cryptocurrencies
SELECT * FROM my_coinmarketcap.listings LIMIT 100;

-- Get cryptocurrencies with specific market cap range
SELECT name, symbol, price, market_cap 
FROM my_coinmarketcap.listings 
WHERE market_cap > 1000000000  -- > $1B market cap
ORDER BY market_cap DESC;
```

### 3. Cryptocurrency Information (`info`)

Get detailed information about specific cryptocurrencies:

```sql
-- Get detailed Bitcoin information
SELECT * FROM my_coinmarketcap.info WHERE symbol = 'BTC';

-- Get information for multiple cryptocurrencies
SELECT symbol, name, description, category, logo
FROM my_coinmarketcap.info 
WHERE symbol IN ('BTC', 'ETH', 'ADA');
```

### 4. Global Metrics (`global_metrics`)

Get global cryptocurrency market metrics:

```sql
-- Get global market overview
SELECT 
    total_cryptocurrencies,
    active_cryptocurrencies,
    total_market_cap,
    total_volume_24h,
    btc_dominance,
    eth_dominance
FROM my_coinmarketcap.global_metrics;
```

## Machine Learning Examples

### Price Prediction Model

Create a model to predict cryptocurrency prices:

```sql
-- Create a prediction model for Bitcoin price
CREATE MODEL bitcoin_price_predictor
FROM my_coinmarketcap.quotes
PREDICT price
WHERE symbol = 'BTC';

-- Make predictions
SELECT price, percent_change_24h, market_cap
FROM bitcoin_price_predictor
WHERE symbol = 'BTC';
```

### Market Trend Analysis

```sql
-- Create a model to predict market trends
CREATE MODEL crypto_trend_predictor
FROM my_coinmarketcap.quotes
PREDICT percent_change_24h
WHERE cmc_rank <= 100;

-- Analyze trends for top cryptocurrencies
SELECT 
    symbol,
    name,
    price,
    percent_change_24h as predicted_change
FROM crypto_trend_predictor
WHERE cmc_rank <= 20;
```

## Available Data Columns

### Quotes Table
- `id`: CoinMarketCap ID
- `name`: Cryptocurrency name
- `symbol`: Cryptocurrency symbol
- `slug`: URL slug
- `cmc_rank`: Market cap ranking
- `price`: Current price in USD
- `volume_24h`: 24-hour trading volume
- `percent_change_1h`: 1-hour price change
- `percent_change_24h`: 24-hour price change
- `percent_change_7d`: 7-day price change
- `market_cap`: Market capitalization
- `circulating_supply`: Circulating supply
- `total_supply`: Total supply
- `max_supply`: Maximum supply

### Info Table
- `id`: CoinMarketCap ID
- `name`: Cryptocurrency name
- `symbol`: Cryptocurrency symbol
- `description`: Detailed description
- `category`: Category (e.g., "Coin", "Token")
- `logo`: Logo URL
- `twitter_username`: Twitter handle
- `platform`: Blockchain platform

### Global Metrics Table
- `total_cryptocurrencies`: Total number of cryptocurrencies
- `active_cryptocurrencies`: Number of active cryptocurrencies
- `total_market_cap`: Total market capitalization
- `total_volume_24h`: Total 24-hour volume
- `btc_dominance`: Bitcoin market dominance percentage
- `eth_dominance`: Ethereum market dominance percentage

## Rate Limits

CoinMarketCap API has rate limits based on your subscription plan:

- **Basic (Free)**: 333 requests/day, 10,000 requests/month
- **Hobbyist**: 3,333 requests/day, 100,000 requests/month
- **Startup**: 16,666 requests/day, 500,000 requests/month
- **Standard**: 33,333 requests/day, 1,000,000 requests/month
- **Professional**: 100,000 requests/day, 3,000,000 requests/month
- **Enterprise**: Custom limits

## Error Handling

The handler includes comprehensive error handling for common issues:

- **Invalid API Key**: Check your API key and ensure it's correctly configured
- **Rate Limit Exceeded**: Upgrade your plan or reduce query frequency
- **Network Issues**: The handler will retry failed requests
- **Invalid Parameters**: Clear error messages for incorrect query parameters

## Troubleshooting

### Common Issues

1. **"Invalid API Key" Error**
   - Verify your API key is correct
   - Check if your API key has the necessary permissions
   - Ensure you're not using the sandbox key in production

2. **"Rate Limit Exceeded" Error**
   - Check your current usage in the CoinMarketCap dashboard
   - Consider upgrading your plan
   - Implement caching for frequently accessed data

3. **"Connection Failed" Error**
   - Check your internet connection
   - Verify the CoinMarketCap API is not down
   - Try using the sandbox environment for testing

### Debug Mode

Enable debug logging to troubleshoot issues:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

We welcome contributions to improve this handler! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/mindsdb-coinmarketcap-handler.git
cd mindsdb-coinmarketcap-handler
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e .
pip install pytest black flake8
```

4. Run tests:
```bash
pytest tests/
```

## Support

For support and questions:

- Open an issue on [GitHub](https://github.com/your-username/mindsdb-coinmarketcap-handler/issues)
- Check the [MindsDB Documentation](https://docs.mindsdb.com/)
- Join the [MindsDB Community](https://mindsdb.com/joincommunity)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [CoinMarketCap](https://coinmarketcap.com/) for providing the cryptocurrency data API
- [MindsDB](https://mindsdb.com/) for the excellent ML platform and handler framework
- The open-source community for continuous improvements and feedback