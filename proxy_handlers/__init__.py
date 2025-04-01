# Import the proxy handlers
from .smartproxy import SmartproxyRotator
from .custom import CustomProxyRotator

__all__ = ['SmartproxyRotator', 'CustomProxyRotator']