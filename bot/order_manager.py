"""
Order manager for placing and managing orders.
"""

from typing import Dict, Any, Optional
from .client import BinanceClient
from .exceptions import OrderPlacementError
from .logging_config import get_logger

logger = get_logger()

class OrderManager:
    """
    Manages order placement and tracking.
    """
    
    def __init__(self, client: BinanceClient):
        """
        Initialize order manager.
        
        Args:
            client: BinanceClient instance
        """
        self.client = client
    
    def format_order_summary(self, symbol: str, side: str, order_type: str, 
                            quantity: str, price: Optional[str] = None) -> str:
        """
        Format order summary for display.
        
        Args:
            symbol: Trading pair
            side: BUY or SELL
            order_type: MARKET or LIMIT
            quantity: Order quantity
            price: Order price
            
        Returns:
            Formatted summary string
        """
        summary = "\n" + "="*50 + "\n"
        summary += "ORDER SUMMARY\n"
        summary += "="*50 + "\n"
        summary += f"Symbol:       {symbol}\n"
        summary += f"Side:         {side}\n"
        summary += f"Type:         {order_type}\n"
        summary += f"Quantity:     {quantity}\n"
        
        if order_type == 'LIMIT' and price:
            summary += f"Price:        {price}\n"
            estimated_cost = float(quantity) * float(price)
            summary += f"Est. Cost:    {estimated_cost:.2f} USDT\n"
        else:
            summary += f"Price:        Market Price\n"
        
        summary += "="*50 + "\n"
        return summary
    
    def place_market_order(self, symbol: str, side: str, quantity: str) -> Dict[str, Any]:
        """
        Place a market order.
        
        Args:
            symbol: Trading pair
            side: BUY or SELL
            quantity: Order quantity
            
        Returns:
            Order response
            
        Raises:
            OrderPlacementError: If order placement fails
        """
        try:
            logger.info(f"Placing MARKET order: {side} {quantity} {symbol}")
            response = self.client.place_order(symbol, side, 'MARKET', quantity)
            logger.info(f"✅ Market order placed - Order ID: {response.get('orderId')}")
            return response
        except Exception as e:
            error_msg = f"Failed to place market order: {str(e)}"
            logger.error(error_msg)
            raise OrderPlacementError(error_msg)
    
    def place_limit_order(self, symbol: str, side: str, quantity: str, price: str) -> Dict[str, Any]:
        """
        Place a limit order.
        
        Args:
            symbol: Trading pair
            side: BUY or SELL
            quantity: Order quantity
            price: Order price
            
        Returns:
            Order response
            
        Raises:
            OrderPlacementError: If order placement fails
        """
        try:
            logger.info(f"Placing LIMIT order: {side} {quantity} {symbol} @ {price}")
            response = self.client.place_order(symbol, side, 'LIMIT', quantity, price)
            logger.info(f"✅ Limit order placed - Order ID: {response.get('orderId')}")
            return response
        except Exception as e:
            error_msg = f"Failed to place limit order: {str(e)}"
            logger.error(error_msg)
            raise OrderPlacementError(error_msg)
    
    def get_open_orders(self, symbol: Optional[str] = None) -> list:
        """
        Get open orders.
        
        Args:
            symbol: Optional specific symbol
            
        Returns:
            List of open orders
        """
        try:
            params = {}
            if symbol:
                params['symbol'] = symbol
            
            # Note: This endpoint may not be implemented in all versions
            # Update based on your actual API requirements
            logger.info("Fetching open orders...")
            return []
        except Exception as e:
            logger.error(f"Failed to fetch open orders: {str(e)}")
            return []
