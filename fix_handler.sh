#!/bin/bash

echo "=== Fixing CoinMarketCap Handler Issues ==="

# 1. Fix the HANDLER_TYPE.DATA issue in __init__.py
echo "1. Fixing HANDLER_TYPE.DATA import and usage..."
sed -i '1i from mindsdb.integrations.libs.const import HANDLER_TYPE' __init__.py
sed -i "s/type = 'data'/type = HANDLER_TYPE.DATA/" __init__.py

# 2. Clean up excessive logging in __init__.py
echo "2. Cleaning up excessive logging..."
sed -i '/^import logging$/d' __init__.py
sed -i '/^logging.basicConfig/d' __init__.py
sed -i '/^logger = logging.getLogger/d' __init__.py
sed -i '/^logger.debug.*Loading CoinMarketCap/d' __init__.py
sed -i '/logger.debug.*Successfully imported/d' __init__.py
sed -i '/logger.error.*Failed to import/d' __init__.py

# 3. Check if we need to create proper MindsDB structure
echo "3. Checking MindsDB handler structure..."
if [ ! -d "mindsdb" ]; then
    echo "Creating proper MindsDB directory structure..."
    mkdir -p mindsdb/integrations/handlers/coinmarketcap_handler
    
    # Move files to proper location
    cp *.py mindsdb/integrations/handlers/coinmarketcap_handler/
    cp *.svg mindsdb/integrations/handlers/coinmarketcap_handler/
    cp requirements.txt mindsdb/integrations/handlers/coinmarketcap_handler/
fi

echo "4. Verifying Python syntax..."
python -m py_compile __init__.py
python -m py_compile coinmarketcap_handler.py
python -m py_compile connection_args.py

echo "=== Handler fixes completed ==="
