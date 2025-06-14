# CoinMarketCap Handler

The CoinMarketCap handler for MindsDB provides seamless integration with the CoinMarketCap API, enabling you to access real-time cryptocurrency market data, prices, and metrics directly from your MindsDB instance.

## Implementation

This handler is implemented using the CoinMarketCap API and provides access to cryptocurrency market data through SQL queries.

## CoinMarketCap API

CoinMarketCap is a leading cryptocurrency data provider that offers comprehensive market data, prices, and information for thousands of cryptocurrencies. The API provides real-time and historical data for cryptocurrency analysis and trading.

## Connection

### Required Parameters

- `api_key`: Your CoinMarketCap API key (required)

### Optional Parameters  

- `sandbox`: Set to `true` to use the sandbox environment for testing (default: `false`)

### Get Your API Key

1. Sign up at [CoinMarketCap Developer Portal](https://coinmarketcap.com/api/)
2. Navigate to your API dashboard
3. Copy your API key

### Example Connection

```sql
CREATE DATABASE coinmarketcap_datasource
WITH 
  ENGINE = 'coinmarketcap',
  PARAMETERS = {
    "api_key": "your_coinmarketcap_api_key_here"
  };
```

For testing with sandbox:

```sql
CREATE DATABASE coinmarketcap_sandbox
WITH 
  ENGINE = 'coinmarketcap',
  PARAMETERS = {
    "api_key": "your_sandbox_api_key",
    "sandbox": true
  };
```

## Usage

### Available Tables

The CoinMarketCap handler provides access to the following tables:

- `quotes` - Real-time cryptocurrency quotes and prices
- `listings` - Cryptocurrency listings with market data
- `info` - Detailed cryptocurrency information
- `global_metrics` - Global cryptocurrency market metrics

### Basic Queries

#### Get Bitcoin Price

```sql
SELECT symbol, name, price, market_cap, percent_change_24h
FROM coinmarketcap_datasource.quotes 
WHERE symbol = 'BTC';
```

#### Get Multiple Cryptocurrencies

```sql
SELECT symbol, name, price, market_cap, percent_change_24h 
FROM coinmarketcap_datasource.quotes 
WHERE symbol IN ('BTC', 'ETH', 'ADA', 'SOL');
```

#### Get Top Cryptocurrencies by Market Cap

```sql
SELECT symbol, name, price, market_cap, cmc_rank
FROM coinmarketcap_datasource.quotes 
ORDER BY cmc_rank 
LIMIT 50;
```

#### Get Global Market Metrics

```sql
SELECT 
    total_cryptocurrencies,
    active_cryptocurrencies,
    total_market_cap,
    total_volume_24h,
    btc_dominance,
    eth_dominance
FROM coinmarketcap_datasource.global_metrics;
```

#### Get Detailed Cryptocurrency Information

```sql
SELECT symbol, name, description, category, logo
FROM coinmarketcap_datasource.info 
WHERE symbol = 'BTC';
```

### Machine Learning Examples

#### Price Prediction Model

```sql
-- Create a model to predict Bitcoin price movements
CREATE MODEL bitcoin_price_predictor
FROM coinmarketcap_datasource.quotes
PREDICT percent_change_24h
WHERE symbol = 'BTC';

-- Make predictions
SELECT 
    symbol,
    price,
    percent_change_24h as predicted_change
FROM bitcoin_price_predictor
WHERE symbol = 'BTC';
```

#### Market Trend Analysis

```sql
-- Create a model to analyze market trends
CREATE MODEL crypto_market_trends
FROM coinmarketcap_datasource.quotes
PREDICT market_cap
WHERE cmc_rank <= 100;

-- Analyze top cryptocurrencies
SELECT 
    symbol,
    name,
    price,
    market_cap as predicted_market_cap
FROM crypto_market_trends
WHERE cmc_rank <= 20;
```

## Supported Columns

### Quotes Table

| Column | Description |
|--------|-------------|
| `id` | CoinMarketCap ID |
| `name` | Cryptocurrency name |
| `symbol` | Cryptocurrency symbol |
| `slug` | URL slug |
| `cmc_rank` | Market cap ranking |
| `price` | Current price in USD |
| `volume_24h` | 24-hour trading volume |
| `percent_change_1h` | 1-hour price change |
| `percent_change_24h` | 24-hour price change |
| `percent_change_7d` | 7-day price change |
| `market_cap` | Market capitalization |
| `circulating_supply` | Circulating supply |
| `total_supply` | Total supply |
| `max_supply` | Maximum supply |

### Info Table

| Column | Description |
|--------|-------------|
| `id` | CoinMarketCap ID |
| `name` | Cryptocurrency name |
| `symbol` | Cryptocurrency symbol |
| `description` | Detailed description |
| `category` | Category (e.g., "Coin", "Token") |
| `logo` | Logo URL |
| `twitter_username` | Official Twitter handle |
| `platform` | Blockchain platform |

### Global Metrics Table

| Column | Description |
|--------|-------------|
| `total_cryptocurrencies` | Total number of cryptocurrencies |
| `active_cryptocurrencies` | Number of active cryptocurrencies |
| `total_market_cap` | Total market capitalization |
| `total_volume_24h` | Total 24-hour volume |
| `btc_dominance` | Bitcoin market dominance percentage |
| `eth_dominance` | Ethereum market dominance percentage |

## Rate Limits

CoinMarketCap API has different rate limits based on your subscription plan:

- **Basic (Free)**: 333 requests/day, 10,000 requests/month
- **Hobbyist**: 3,333 requests/day, 100,000 requests/month  
- **Startup**: 16,666 requests/day, 500,000 requests/month
- **Standard**: 33,333 requests/day, 1,000,000 requests/month
- **Professional**: 100,000 requests/day, 3,000,000 requests/month
- **Enterprise**: Custom limits

## Troubleshooting

### Common Issues

**"Invalid API Key" Error**
- Verify your API key is correct
- Check if your API key has the necessary permissions
- Ensure you're not using the sandbox key in production

**"Rate Limit Exceeded" Error**  
- Check your current usage in the CoinMarketCap dashboard
- Consider upgrading your plan
- Implement caching for frequently accessed data

**"Connection Failed" Error**
- Check your internet connection
- Verify the CoinMarketCap API is not down
- Try using the sandbox environment for testing

## Resources

- [CoinMarketCap API Documentation](https://coinmarketcap.com/api/documentation/v1/)
- [MindsDB Documentation](https://docs.mindsdb.com/)
- [CoinMarketCap Developer Portal](https://coinmarketcap.com/api/) 