import random
import requests
import time
from urllib.parse import urlparse

class SmartproxyRotator:
    """A proxy rotator for Smartproxy service."""
    
    def __init__(self, username, password, endpoint='gate.smartproxy.com', port=7000, country=None):
        """Initialize the Smartproxy rotator.
        
        Args:
            username (str): Your Smartproxy username.
            password (str): Your Smartproxy password.
            endpoint (str, optional): Smartproxy endpoint. Default is 'gate.smartproxy.com'.
            port (int, optional): Smartproxy port. Default is 7000.
            country (str, optional): Country code for geo-targeting (e.g., 'us', 'uk').
                Default is None (random country).
        """
        self.username = username
        self.password = password
        self.endpoint = endpoint
        self.port = port
        self.country = country
        self.session_id = None
        self.last_rotation = 0
        self.rotation_interval = 60  # Rotate every 60 seconds by default
    
    def get_proxy(self, force_new=False):
        """Get a proxy configuration for use with Playwright.
        
        Args:
            force_new (bool, optional): Force a new proxy even if the rotation interval
                hasn't elapsed. Default is False.
        
        Returns:
            dict: A proxy configuration dictionary for Playwright.
        """
        # Check if we need to rotate the proxy
        current_time = time.time()
        if force_new or self.session_id is None or (current_time - self.last_rotation) > self.rotation_interval:
            # Generate a new session ID
            self.session_id = str(random.randint(10000, 99999))
            self.last_rotation = current_time
        
        # Construct the proxy URL
        proxy_url = f"http://{self.username}-session-{self.session_id}:{self.password}@{self.endpoint}:{self.port}"
        
        # Add country if specified
        if self.country:
            proxy_url = f"http://{self.username}-country-{self.country}-session-{self.session_id}:{self.password}@{self.endpoint}:{self.port}"
        
        # Return the proxy configuration for Playwright
        return {
            'server': proxy_url,
            'username': f"{self.username}-session-{self.session_id}",
            'password': self.password
        }
    
    def rotate_proxy(self):
        """Force a proxy rotation.
        
        Returns:
            dict: A new proxy configuration dictionary.
        """
        return self.get_proxy(force_new=True)
    
    def test_proxy(self, test_url='https://api.ipify.org?format=json'):
        """Test the proxy connection.
        
        Args:
            test_url (str, optional): URL to test the proxy with.
                Default is 'https://api.ipify.org?format=json'.
        
        Returns:
            dict: Test result with status and IP information.
        """
        proxy = self.get_proxy()
        proxies = {
            'http': proxy['server'],
            'https': proxy['server']
        }
        
        try:
            response = requests.get(test_url, proxies=proxies, timeout=10)
            if response.status_code == 200:
                return {
                    'success': True,
                    'ip': response.json().get('ip', 'Unknown'),
                    'status_code': response.status_code
                }
            else:
                return {
                    'success': False,
                    'error': f"HTTP Error: {response.status_code}",
                    'status_code': response.status_code
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def set_rotation_interval(self, seconds):
        """Set the automatic proxy rotation interval.
        
        Args:
            seconds (int): Interval in seconds between automatic rotations.
        """
        self.rotation_interval = seconds