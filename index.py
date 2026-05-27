"""
Binance Futures Trading Bot - Project Index
============================================

This file serves as an index and quick reference guide for the project structure
and available modules.

PROJECT STRUCTURE:
==================
.
├── main.py                      # Entry point - Run this to start the bot
├── index.py                     # This file - Project index and reference
├── requirements.txt             # Project dependencies
├── .env.example                 # Environment variables template
├── README.md                    # Project documentation
├── .gitignore                   # Git ignore configuration
├── logs/                        # Log files directory (auto-created)
│   └── trading_bot.log         # Main log file
└── bot/                        # Bot package
    ├── __init__.py             # Package initialization and exports
    ├── client.py               # Binance API client
    ├── order_manager.py        # Order management and placement
    ├── validators.py           # Input validation functions
    ├── exceptions.py           # Custom exception classes
    └── logging_config.py       # Logging configuration

MODULES OVERVIEW:
=================

1. bot.client (BinanceClient)
   - Handles all Binance Futures API interactions
   - Methods: test_connectivity(), place_order(), get_account_info(), etc.
   - Supports both MARKET and LIMIT orders

2. bot.order_manager (OrderManager)
   - Manages order lifecycle and placement
   - Methods: place_market_order(), place_limit_order(), format_order_summary()
   - Provides user-friendly order formatting

3. bot.validators
   - Validates order parameters before placement
   - Function: validate_order_params()
   - Checks: symbol format, side, order type, quantity, price

4. bot.exceptions
   - Custom exception hierarchy:
     * ValidationError - Raised for invalid input
     * BinanceAPIError - Raised for API failures
     * OrderPlacementError - Raised for order placement issues
     * ConfigurationError - Raised for configuration issues

5. bot.logging_config
   - Sets up logging to both file and console
   - Functions: setup_logging(), get_logger()
   - Log file location: logs/trading_bot.log

QUICK START COMMANDS:
====================

Interactive Mode (Recommended):
    python main.py

Market Order via CLI:
    python main.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001

Limit Order via CLI:
    python main.py --symbol ETHUSDT --side SELL --order-type LIMIT --quantity 0.01 --price 3000

AVAILABLE CLI ARGUMENTS:
=======================
--symbol TEXT       Trading pair (e.g., BTCUSDT, ETHUSDT) [required]
--side TEXT        Order direction: BUY or SELL [required]
--order-type TEXT  Order type: MARKET or LIMIT [required]
--quantity TEXT    Order quantity in coins [required]
--price TEXT       Order price in USDT [required for LIMIT orders]

SETUP CHECKLIST:
================
[ ] Clone repository: git clone <repo-url>
[ ] Install dependencies: pip install -r requirements.txt
[ ] Create .env file: cp .env.example .env
[ ] Edit .env with Binance Testnet credentials
[ ] Create logs directory: mkdir -p logs
[ ] Run the bot: python main.py

ENVIRONMENT VARIABLES (.env):
=============================
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
TESTNET_URL=https://testnet.binancefuture.com

EXAMPLE USAGE IN PYTHON:
========================

# Import the bot components
from bot import (
    BinanceClient,
    OrderManager,
    validate_order_params,
    setup_logging,
    get_logger
)

# Setup logging
setup_logging()
logger = get_logger()

# Initialize client with credentials
client = BinanceClient(
    api_key="your_key",
    api_secret="your_secret",
    base_url="https://testnet.binancefuture.com"
)

# Test connectivity
client.test_connectivity()

# Create order manager
manager = OrderManager(client)

# Validate parameters
params = validate_order_params(
    symbol="BTCUSDT",
    side="BUY",
    order_type="MARKET",
    quantity="0.001"
)

# Place order
response = manager.place_market_order("BTCUSDT", "BUY", "0.001")

ERROR HANDLING:
===============

try:
    from bot import (
        ValidationError,
        BinanceAPIError,
        OrderPlacementError
    )
except ValidationError as e:
    print(f"Invalid input: {e}")
except BinanceAPIError as e:
    print(f"API error: {e}")
except OrderPlacementError as e:
    print(f"Order failed: {e}")

LOGGING OUTPUT:
===============
- Console output: Real-time logs to terminal
- File output: Detailed logs in logs/trading_bot.log
- Log level: INFO (shows all operations, warnings, and errors)
- Format: timestamp - module - level - message

TROUBLESHOOTING:
================

Q: "Missing API credentials error"
A: Ensure .env file exists with valid BINANCE_API_KEY and BINANCE_API_SECRET

Q: "Connection error"
A: Check internet connection and verify testnet.binancefuture.com is accessible

Q: "Order validation failed"
A: Verify symbol is uppercase (e.g., BTCUSDT), quantity > 0, price > 0 for limit orders

Q: "Invalid symbol format"
A: Symbol must be at least 6 characters (e.g., BTCUSDT, not BTC)

FEATURES:
=========
✅ Market & Limit Orders - Support for both order types
✅ BUY/SELL Operations - Full bidirectional trading
✅ CLI Arguments - Command-line automation
✅ Interactive Mode - User-friendly manual trading
✅ Comprehensive Logging - Detailed operation tracking
✅ Error Handling - Robust exception management
✅ Testnet Only - Safe testing without real funds
✅ Parameter Validation - Pre-flight checks before API calls

SECURITY NOTES:
===============
- Never commit .env file to version control
- Testnet credentials only - no real funds at risk
- API key and secret should be kept confidential
- Always validate before placing orders
- Use testnet for thorough testing

For more information, see README.md
"""

# Import all main components for easy access
from bot import (
    setup_logging,
    get_logger,
    BinanceClient,
    OrderManager,
    validate_order_params,
    ValidationError,
    BinanceAPIError,
    OrderPlacementError,
    ConfigurationError
)

# Print project info if run directly
if __name__ == "__main__":
    print(__doc__)
