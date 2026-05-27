"""
Validators for order parameters.
"""

from .exceptions import ValidationError

def validate_order_params(symbol, side, order_type, quantity, price=None):
    """
    Validate order parameters.
    
    Args:
        symbol: Trading pair (e.g., BTCUSDT)
        side: BUY or SELL
        order_type: MARKET or LIMIT
        quantity: Order quantity
        price: Order price (required for LIMIT orders)
        
    Returns:
        Dictionary with validated parameters
        
    Raises:
        ValidationError: If validation fails
    """
    
    # Validate symbol
    if not symbol or not isinstance(symbol, str):
        raise ValidationError("Symbol must be a non-empty string")
    
    symbol = symbol.upper().strip()
    
    if len(symbol) < 6:
        raise ValidationError(f"Invalid symbol format: {symbol}")
    
    # Validate side
    if side not in ['BUY', 'SELL']:
        raise ValidationError(f"Side must be BUY or SELL, got: {side}")
    
    # Validate order type
    if order_type not in ['MARKET', 'LIMIT']:
        raise ValidationError(f"Order type must be MARKET or LIMIT, got: {order_type}")
    
    # Validate quantity
    if not quantity:
        raise ValidationError("Quantity is required")
    
    try:
        qty_float = float(quantity)
        if qty_float <= 0:
            raise ValidationError("Quantity must be greater than 0")
    except ValueError:
        raise ValidationError(f"Invalid quantity format: {quantity}")
    
    # Validate price for LIMIT orders
    if order_type == 'LIMIT':
        if not price:
            raise ValidationError("Price is required for LIMIT orders")
        
        try:
            price_float = float(price)
            if price_float <= 0:
                raise ValidationError("Price must be greater than 0")
        except ValueError:
            raise ValidationError(f"Invalid price format: {price}")
    
    return {
        'symbol': symbol,
        'side': side,
        'order_type': order_type,
        'quantity': str(qty_float),
        'price': str(float(price)) if price else None
    }
