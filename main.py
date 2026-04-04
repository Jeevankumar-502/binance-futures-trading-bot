#!/usr/bin/env python3
"""
Main entry point for the trading bot.
"""

import sys
import argparse
import os
from dotenv import load_dotenv
from bot import (
    setup_logging,
    get_logger,
    BinanceClient,
    OrderManager,
    validate_order_params,
    ValidationError,
    BinanceAPIError,
    OrderPlacementError
)

# Load environment variables
load_dotenv()

# Setup logging
setup_logging()
logger = get_logger()

def main():
    """Main application entry point."""
    
    parser = argparse.ArgumentParser(
        description="Binance Futures Trading Bot for Testnet",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Place a market order
  python main.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001
  
  # Place a limit order
  python main.py --symbol ETHUSDT --side SELL --order-type LIMIT --quantity 0.01 --price 3000
  
  # Interactive mode
  python main.py
        """
    )
    
    parser.add_argument('--symbol', help='Trading pair (e.g., BTCUSDT)')
    parser.add_argument('--side', choices=['BUY', 'SELL'], help='Order side')
    parser.add_argument('--order-type', dest='order_type', choices=['MARKET', 'LIMIT'], help='Order type')
    parser.add_argument('--quantity', help='Order quantity')
    parser.add_argument('--price', help='Order price (required for LIMIT orders)')
    
    args = parser.parse_args()
    
    # Get inputs (from args or interactive prompt)
    if args.symbol:
        symbol = args.symbol
    else:
        symbol = input("\n📊 Trading Symbol (e.g., BTCUSDT): ").strip()
    
    if args.side:
        side = args.side
    else:
        while True:
            side = input("📈 Order Side (BUY/SELL): ").strip().upper()
            if side in ['BUY', 'SELL']:
                break
            print("❌ Invalid side. Please enter BUY or SELL")
    
    if args.order_type:
        order_type = args.order_type
    else:
        while True:
            order_type = input("🔄 Order Type (MARKET/LIMIT): ").strip().upper()
            if order_type in ['MARKET', 'LIMIT']:
                break
            print("❌ Invalid order type. Please enter MARKET or LIMIT")
    
    if args.quantity:
        quantity = args.quantity
    else:
        quantity = input("📦 Quantity: ").strip()
    
    price = None
    if order_type == 'LIMIT':
        if args.price:
            price = args.price
        else:
            price = input("💰 Price: ").strip()
    elif args.price:
        price = args.price  # In case price was provided for market order
    
    try:
        logger.info("Starting trading bot...")
        logger.info(f"User input - Symbol: {symbol}, Side: {side}, Type: {order_type}, Qty: {quantity}, Price: {price}")
        
        # Validate inputs
        print("\n⏳ Validating order parameters...")
        logger.info("Validating order parameters...")
        
        validated = validate_order_params(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
        
        print("✅ Parameters validated successfully\n")
        logger.info("✅ Parameters validated successfully")
        
        # Get API credentials
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")
        testnet_url = os.getenv("TESTNET_URL", "https://testnet.binancefuture.com")
        
        if not api_key or not api_secret:
            raise BinanceAPIError(
                "Missing API credentials. Please set BINANCE_API_KEY and BINANCE_API_SECRET in .env file"
            )
        
        # Initialize client and manager
        print("⏳ Initializing Binance client...")
        logger.info("Initializing Binance client...")
        client = BinanceClient(api_key, api_secret, testnet_url)
        manager = OrderManager(client)
        
        # Test connection
        print("⏳ Testing API connectivity...")
        logger.info("Testing API connectivity...")
        client.test_connectivity()
        print("✅ API connection successful\n")
        logger.info("✅ API connection successful")
        
        # Display order summary
        summary = manager.format_order_summary(
            validated["symbol"],
            validated["side"],
            validated["order_type"],
            validated["quantity"],
            validated.get("price")
        )
        print(summary)
        
        # Confirm order
        confirm = input("Do you want to proceed with this order? (yes/no): ").strip().lower()
        if confirm not in ['yes', 'y']:
            logger.info("Order cancelled by user")
            print("❌ Order cancelled")
            return
        
        # Place order
        print("\n⏳ Placing order...")
        logger.info("Placing order...")
        
        if validated["order_type"] == "MARKET":
            response = manager.place_market_order(
                validated["symbol"],
                validated["side"],
                validated["quantity"]
            )
        else:  # LIMIT
            response = manager.place_limit_order(
                validated["symbol"],
                validated["side"],
                validated["quantity"],
                validated["price"]
            )
        
        # Display response
        print("\n" + "="*50)
        print("ORDER RESPONSE")
        print("="*50)
        print(f"Order ID:           {response.get('orderId', 'N/A')}")
        print(f"Status:             {response.get('status', 'N/A')}")
        print(f"Executed Quantity:  {response.get('executedQty', '0')}")
        print(f"Average Price:      {response.get('avgPrice', 'N/A')}")
        print("="*50)
        
        logger.info("✅ Order placement completed successfully")
        print("\n✅ Order placed successfully!")
        print(f"📋 Check logs/trading_bot.log for details")
    
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        print(f"\n❌ Validation Error: {str(e)}")
        sys.exit(1)
    
    except BinanceAPIError as e:
        logger.error(f"API error: {str(e)}")
        print(f"\n❌ API Error: {str(e)}")
        sys.exit(1)
    
    except OrderPlacementError as e:
        logger.error(f"Order placement error: {str(e)}")
        print(f"\n❌ Order Placement Error: {str(e)}")
        sys.exit(1)
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()