# Binance Futures Testnet Trading Bot

## 🚀 Features
- Market & Limit Orders
- BUY / SELL support
- CLI-based input
- Logging to file
- Error handling

## 🛠 Setup

1. Clone repo
2. Install dependencies:

   pip install -r requirements.txt

3. Create `.env` file:

   BINANCE_API_KEY=your_key
   BINANCE_API_SECRET=your_secret

4. Run bot:

   python main.py \
     --symbol BTCUSDT \
     --side BUY \
     --order_type MARKET \
     --quantity 0.01

## 📌 Limit Order Example

   python main.py \
     --symbol BTCUSDT \
     --side SELL \
     --order_type LIMIT \
     --quantity 0.01 \
     --price 60000

## 📄 Logs
- Stored in `bot.log`

## ⚠️ Notes
- Uses Binance Futures Testnet
- No real funds involved

