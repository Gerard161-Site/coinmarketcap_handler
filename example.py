
import os
from mindsdb import MindsDB

# Initialize MindsDB
mdb = MindsDB()

def setup_coinmarketcap_connection():
    """Set up connection to CoinMarketCap API."""
    api_key = os.getenv('COINMARKETCAP_API_KEY')
    if not api_key:
        print("Please set COINMARKETCAP_API_KEY environment variable")
        return False
    
    # Create database connection
    mdb.databases.create(
        'my_coinmarketcap',
        engine='coinmarketcap',
        parameters={
            'api_key': api_key
        }
    )
    print("CoinMarketCap connection created successfully!")
    return True

def fetch_crypto_data():
    """Fetch cryptocurrency data examples."""
    print("\\n=== Fetching Cryptocurrency Data ===")
    
    # Get Bitcoin data
    btc_data = mdb.query("SELECT * FROM my_coinmarketcap.quotes WHERE symbol = 'BTC'")
    print(f"Bitcoin Price: ${btc_data.iloc[0]['price']:.2f}")
    
    # Get top 10 cryptocurrencies
    top_10 = mdb.query("""
        SELECT symbol, name, price, market_cap, percent_change_24h 
        FROM my_coinmarketcap.listings 
        ORDER BY cmc_rank 
        LIMIT 10
    """)
    print("\\nTop 10 Cryptocurrencies:")
    print(top_10)
    
    # Get global metrics
    global_metrics = mdb.query("SELECT * FROM my_coinmarketcap.global_metrics")
    print(f"\\nTotal Market Cap: ${global_metrics.iloc[0]['total_market_cap']:,.0f}")
    print(f"Bitcoin Dominance: {global_metrics.iloc[0]['btc_dominance']:.1f}%")

def create_price_prediction_model():
    """Create a cryptocurrency price prediction model."""
    print("\\n=== Creating Price Prediction Model ===")
    
    # Create model for Bitcoin price prediction
    mdb.query("""
        CREATE MODEL bitcoin_price_predictor
        FROM my_coinmarketcap.quotes
        PREDICT price
        WHERE symbol = 'BTC'
    """)
    print("Bitcoin price prediction model created!")
    
    # Make prediction
    prediction = mdb.query("""
        SELECT price as predicted_price, percent_change_24h
        FROM bitcoin_price_predictor
        WHERE symbol = 'BTC'
    """)
    print(f"Predicted Bitcoin Price: ${prediction.iloc[0]['predicted_price']:.2f}")

def create_market_trend_model():
    """Create a market trend prediction model."""
    print("\\n=== Creating Market Trend Model ===")
    
    # Create model for market trend prediction
    mdb.query("""
        CREATE MODEL crypto_trend_predictor
        FROM my_coinmarketcap.quotes
        PREDICT percent_change_24h
        WHERE cmc_rank <= 100
    """)
    print("Crypto trend prediction model created!")
    
    # Analyze trends for top cryptocurrencies
    trends = mdb.query("""
        SELECT symbol, name, percent_change_24h as predicted_change
        FROM crypto_trend_predictor
        WHERE cmc_rank <= 10
    """)
    print("\\nPredicted 24h Changes for Top 10 Cryptos:")
    print(trends)

def main():
    """Main function to run all examples."""
    print("CoinMarketCap Handler Usage Examples")
    print("===================================")
    
    # Setup connection
    if not setup_coinmarketcap_connection():
        return
    
    try:
        # Fetch data examples
        fetch_crypto_data()
        
        # ML model examples
        create_price_prediction_model()
        create_market_trend_model()
        
        print("\\n=== All examples completed successfully! ===")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure MindsDB is running and your API key is valid.")

if __name__ == "__main__":
    main()