"""
Binance Futures API Client for Testnet
"""

import requests
import hmac
import hashlib
import time
from typing import Dict, Any, Optional
from urllib.parse import urlencode
from .logging_config import get_logger
from .exceptions import BinanceAPIError

logger = get_logger()

class BinanceClient:
    """
    Client for interacting with Binance Futures Testnet API.
    """
    
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://testnet.binancefuture.com"):
        """
        Initialize Binance client.
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            base_url: Base URL for API (testnet or mainnet)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'X-MBX-APIKEY': api_key,
            'Content-Type': 'application/x-www-form-urlencoded'
        })
    
    def _generate_signature(self, query_string: str) -> str:
        """
        Generate HMAC SHA256 signature.
        
        Args:
            query_string: Query string to sign
            
        Returns:
            HMAC signature
        """
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def _request(self, method: str, endpoint: str, signed: bool = False, 
                 params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make HTTP request to Binance API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            signed: Whether to sign the request
            params: Query parameters
            
        Returns:
            API response as dictionary
            
        Raises:
            BinanceAPIError: If API request fails
        """
        url = f"{self.base_url}{endpoint}"
        params = params or {}
        
        if signed:
            params['timestamp'] = int(time.time() * 1000)
            query_string = urlencode(params)
            params['signature'] = self._generate_signature(query_string)
        
        try:
            logger.info(f"Making {method} request to {endpoint}")
            
            if method == 'GET':
                response = self.session.get(url, params=params, timeout=10)
            elif method == 'POST':
                response = self.session.post(url, params=params, timeout=10)
            elif method == 'DELETE':
                response = self.session.delete(url, params=params, timeout=10)
            else:
                raise BinanceAPIError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            
            data = response.json()
            
            # Check for API errors in response
            if 'code' in data and data['code'] != 200:
                error_msg = data.get('msg', 'Unknown error')
                raise BinanceAPIError(f"API Error {data['code']}: {error_msg}")
            
            return data
            
        except requests.exceptions.Timeout:
            raise BinanceAPIError("Request timeout - API server not responding")
        except requests.exceptions.ConnectionError:
            raise BinanceAPIError("Connection error - unable to reach API")
        except requests.exceptions.HTTPError as e:
            try:
                error_data = e.response.json()
                error_msg = error_data.get('msg', str(e))
            except:
                error_msg = str(e)
            raise BinanceAPIError(f"HTTP Error: {error_msg}")
        except Exception as e:
            raise BinanceAPIError(f"Request failed: {str(e)}")
    
    def test_connectivity(self) -> Dict[str, Any]:
        """
        Test connectivity to Binance API.
        
        Returns:
            Test response
            
        Raises:
            BinanceAPIError: If connectivity test fails
        """
        try:
            logger.info("Testing API connectivity...")
            response = self._request('GET', '/fapi/v1/ping')
            logger.info("✅ Connectivity test successful")
            return response
        except Exception as e:
            logger.error(f"Connectivity test failed: {str(e)}")
            raise
    
    def get_exchange_info(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """
        Get exchange information.
        
        Args:
            symbol: Optional specific symbol
            
        Returns:
            Exchange info
            
        Raises:
            BinanceAPIError: If request fails
        """
        try:
            params = {}
            if symbol:
                params['symbol'] = symbol
            
            response = self._request('GET', '/fapi/v1/exchangeInfo', params=params)
            return response
        except Exception as e:
            logger.error(f"Failed to get exchange info: {str(e)}")
            raise
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Get account information.
        
        Returns:
            Account info
            
        Raises:
            BinanceAPIError: If request fails
        """
        try:
            logger.info("Fetching account information...")
            response = self._request('GET', '/fapi/v2/account', signed=True)
            return response
        except Exception as e:
            logger.error(f"Failed to get account info: {str(e)}")
            raise
    
    def place_order(self, symbol: str, side: str, order_type: str, 
                    quantity: str, price: Optional[str] = None,
                    time_in_force: str = 'GTC') -> Dict[str, Any]:
        """
        Place an order.
        
        Args:
            symbol: Trading pair
            side: BUY or SELL
            order_type: MARKET or LIMIT
            quantity: Order quantity
            price: Order price (required for LIMIT orders)
            time_in_force: Time in force (GTC, IOC, FOK)
            
        Returns:
            Order response
            
        Raises:
            BinanceAPIError: If order placement fails
        """
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity
        }
        
        if order_type == 'LIMIT':
            if not price:
                raise BinanceAPIError("Price is required for LIMIT orders")
            params['price'] = price
            params['timeInForce'] = time_in_force
        
        try:
            logger.info(f"Placing {order_type} {side} order for {symbol}")
            response = self._request('POST', '/fapi/v1/order', signed=True, params=params)
            logger.info(f"Order placed successfully - Order ID: {response.get('orderId')}")
            return response
        except Exception as e:
            logger.error(f"Failed to place order: {str(e)}")
            raise
    
    def get_open_orders(self, symbol: Optional[str] = None) -> list:
        """
        Get open orders.
        
        Args:
            symbol: Optional specific symbol
            
        Returns:
            List of open orders
            
        Raises:
            BinanceAPIError: If request fails
        """
        try:
            params = {}
            if symbol:
                params['symbol'] = symbol
            
            response = self._request('GET', '/fapi/v1/openOrders', signed=True, params=params)
            return response if isinstance(response, list) else []
        except Exception as e:
            logger.error(f"Failed to get open orders: {str(e)}")
            return []
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Cancel an order.
        
        Args:
            symbol: Trading pair
            order_id: Order ID to cancel
            
        Returns:
            Cancellation response
            
        Raises:
            BinanceAPIError: If cancellation fails
        """
        params = {
            'symbol': symbol,
            'orderId': order_id
        }
        
        try:
            logger.info(f"Cancelling order {order_id} for {symbol}")
            response = self._request('DELETE', '/fapi/v1/order', signed=True, params=params)
            logger.info(f"Order cancelled successfully")
            return response
        except Exception as e:
            logger.error(f"Failed to cancel order: {str(e)}")
            raise
