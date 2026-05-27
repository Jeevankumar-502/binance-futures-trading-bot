"""
Custom exception classes for the trading bot.
"""

class BotException(Exception):
    """Base exception for the trading bot."""
    pass

class ValidationError(BotException):
    """Raised when validation fails."""
    pass

class BinanceAPIError(BotException):
    """Raised when Binance API returns an error."""
    pass

class OrderPlacementError(BotException):
    """Raised when order placement fails."""
    pass

class ConfigurationError(BotException):
    """Raised when configuration is missing or invalid."""
    pass
