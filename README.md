# Binance Futures Testnet Trading Bot

A Python-based trading bot for Binance Futures Testnet with market and limit order support.

## ✨ Features

- ✅ **Market & Limit Orders** - Place both market and limit orders
- ✅ **BUY/SELL Support** - Execute both buy and sell operations  
- ✅ **CLI Input** - Command-line arguments for automated trading
- ✅ **Interactive Mode** - User-friendly prompts for manual trading
- ✅ **Comprehensive Logging** - Detailed logs to file and console
- ✅ **Error Handling** - Robust exception handling and validation
- ✅ **Testnet Only** - Safe testing without real funds

## 🛠️ Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Jeevankumar-502/binance-futures-trading-bot.git
cd binance-futures-trading-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Create `.env` File
Copy `.env.example` to `.env` and add your Binance Testnet credentials:

```bash
cp .env.example .env
```

Edit `.env` with your credentials from https://testnet.binancefuture.com/:
```
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret
TESTNET_URL=https://testnet.binancefuture.com
```

### 4. Create Logs Directory
```bash 
mkdir -p logs
```

## 🚀 Usage

### Interactive Mode (Recommended for beginners)
```bash
python main.py
```

### Market Order (Command Line)
```bash
python main.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001
```

### Limit Order (Command Line)
```bash
python main.py --symbol ETHUSDT --side SELL --order-type LIMIT --quantity 0.01 --price 3000
```

### Available Arguments
- `--symbol`: Trading pair (e.g., BTCUSDT, ETHUSDT)
- `--side`: Order direction (BUY or SELL)
- `--order-type`: MARKET or LIMIT
- `--quantity`: Order quantity
- `--price`: Price (required for LIMIT orders only)

## 📋 Project Structure

```
.
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── logs/                  # Log files directory
└── bot/
    ├── __init__.py        # Bot module initialization
    ├── client.py          # Binance API client
    ├── order_manager.py   # Order management
    ├── validators.py      # Input validation
    └── logging_config.py  # Logging setup
```

## 📖 How It Works

1. **Initialization**: Loads API credentials from `.env` file
2. **Input Validation**: Validates order parameters (symbol, quantity, price)
3. **Connectivity Test**: Tests Binance API connection
4. **Order Summary**: Displays order details for confirmation
5. **Order Placement**: Sends order to Binance Testnet
6. **Logging**: Records all operations in `logs/trading_bot.log`

## ⚠️ Important Notes

- **Testnet Only**: This bot operates on Binance Futures Testnet - no real funds are used
- **API Credentials**: Get testnet credentials from https://testnet.binancefuture.com/
- **Order Validation**: All orders are validated before placement
- **Error Handling**: Comprehensive error messages for troubleshooting

## 📊 Logging

All operations are logged to `logs/trading_bot.log`:
- API connections
- Order placements
- Validation results
- Errors and exceptions

## 🔧 Troubleshooting

### Missing API Credentials Error
- Ensure `.env` file exists in project root
- Verify `BINANCE_API_KEY` and `BINANCE_API_SECRET` are set
- Check credentials are from Testnet (not Mainnet)

### Connection Errors
- Verify internet connection
- Check Testnet URL is accessible
- Ensure API credentials are valid

### Order Validation Errors
- Symbol must be uppercase (e.g., BTCUSDT)
- Quantity must be greater than 0
- For LIMIT orders, price is required and must be > 0
- Use valid Binance trading pairs

## 📝 License

This project is open source and available under the MIT License.

## ⚡ Quick Start

```bash
# 1. Clone
git clone https://github.com/Jeevankumar-502/binance-futures-trading-bot.git
cd binance-futures-trading-bot

# 2. Install
pip install -r requirements.txt

# 3. Configure
cp .env.example .env
# Edit .env with your testnet credentials

# 4. Create logs directory
mkdir -p logs

# 5. Run
python main.py
```

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## ⚠️ Disclaimer

This bot is for educational purposes. Use at your own risk. Always test thoroughly on testnet before any production use.
