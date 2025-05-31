# CoinMarketCap Handler Installation Guide

This guide explains how to install and set up the CoinMarketCap handler for MindsDB.

## File Structure

Your CoinMarketCap handler should have the following structure:

```
coinmarketcap_handler/
├── __init__.py                    # Handler module initialization
├── __about__.py                   # Handler metadata
├── coinmarketcap_handler.py       # Main handler implementation
├── coinmarketcap_tables.py        # Table implementations
├── connection_args.py             # Connection arguments definition
├── requirements.txt               # Python dependencies
├── README.md                      # Handler documentation
├── setup.py                       # Package setup file
├── example_usage.py               # Usage examples
├── test_coinmarketcap_handler.py  # Unit tests
└── icon.svg                       # Handler icon (optional)
```

## Installation Methods

### Method 1: Direct Installation in MindsDB Source

If you have MindsDB installed from source:

1. **Navigate to handlers directory:**
```bash
cd /path/to/mindsdb/mindsdb/integrations/handlers/
```

2. **Create the handler directory:**
```bash
mkdir coinmarketcap_handler
cd coinmarketcap_handler
```

3. **Copy all the handler files** (created by this guide) into the directory

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Restart MindsDB:**
```bash
cd /path/to/mindsdb
python -m mindsdb
```

### Method 2: Installation via pip (if packaged)

1. **Install the handler package:**
```bash
pip install mindsdb-coinmarketcap-handler
```

2. **Copy to MindsDB handlers directory:**
```bash
# Find your site-packages directory
python -c "import site; print(site.getsitepackages())"

# Copy to MindsDB
cp -r /path/to/site-packages/coinmarketcap_handler /path/to/mindsdb/mindsdb/integrations/handlers/
```

### Method 3: Docker Installation

1. **Create a Dockerfile:**
```dockerfile
FROM mindsdb/mindsdb:latest

# Copy the handler
COPY coinmarketcap_handler /opt/mindsdb/mindsdb/integrations/handlers/coinmarketcap_handler/

# Install dependencies
RUN pip install requests>=2.25.0 pandas>=1.3.0

EXPOSE 47334 47335

CMD ["python", "-m", "mindsdb"]
```

2. **Build and run:**
```bash
docker build -t mindsdb-with-coinmarketcap .
docker run -p 47334:47334 -p 47335:47335 mindsdb-with-coinmarketcap
```

### Method 4: Development Setup

For development and testing:

1. **Clone your repository:**
```bash
git clone https://github.com/your-username/mindsdb-coinmarketcap-handler.git
cd mindsdb-coinmarketcap-handler
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install in development mode:**
```bash
pip install -e .
```

4. **Create symlink to MindsDB:**
```bash
ln -s $(pwd)/coinmarketcap_handler /path/to/mindsdb/mindsdb/integrations/handlers/
```

## Verification

After installation, verify the handler is working:

1. **Start MindsDB:**
```bash
python -m mindsdb
```

2. **Check handler availability:**
```sql
SELECT * FROM information_schema.handlers WHERE name = 'coinmarketcap';
```

3. **Test connection:**
```sql
CREATE DATABASE test_coinmarketcap
WITH ENGINE = 'coinmarketcap',
PARAMETERS = {
    "api_key": "your_api_key_here",
    "sandbox": true
};

SELECT * FROM test_coinmarketcap.quotes WHERE symbol = 'BTC';
```

## Troubleshooting

### Common Issues

**1. Handler not found:**
- Check that all files are in the correct directory
- Verify the directory name is `coinmarketcap_handler`
- Restart MindsDB after copying files

**2. Import errors:**
- Install all required dependencies: `pip install -r requirements.txt`
- Check Python version compatibility (3.8+)

**3. API key issues:**
- Verify your CoinMarketCap API key is valid
- Check rate limits on your account
- Try using sandbox mode first

**4. Permission errors:**
- Ensure you have write permissions to the MindsDB directory
- On Linux/Mac, you might need `sudo` for system-wide installations

### Debug Mode

Enable debug logging to troubleshoot:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Dependencies

The handler requires these Python packages:

- `requests>=2.25.0` - For HTTP API calls
- `pandas>=1.3.0` - For data manipulation
- `mindsdb>=23.0.0` - MindsDB core (automatically installed)

## Next Steps

After successful installation:

1. **Get your CoinMarketCap API key** from https://coinmarketcap.com/api/
2. **Follow the usage examples** in the README
3. **Create your first ML model** using cryptocurrency data
4. **Explore advanced features** like time series forecasting

## Support

If you encounter issues:

1. Check the [MindsDB documentation](https://docs.mindsdb.com/)
2. Review the [handler development guide](https://docs.mindsdb.com/contribute/app-handlers)
3. Open an issue on GitHub
4. Join the [MindsDB community](https://mindsdb.com/joincommunity)