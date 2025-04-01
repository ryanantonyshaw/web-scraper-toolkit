import random
import time

class CustomProxyRotator:
    """A proxy rotator for custom proxy lists."""
    
    def __init__(self, proxies=None):
        """Initialize the custom proxy rotator.
        
        Args:
            proxies (list, optional): A list of proxy dictionaries. Each dictionary should have
                at least a 'server' key, and optionally 'username' and 'password' keys.
                Example: [{'server': 'http://proxy1.example.com:8080', 'username': 'user1', 'password': 'pass1'}]
                Default is None (empty list).
        """
        self.proxies = proxies or []
        self.current_index = -1
        self.last_rotation = 0
        self.rotation_interval = 60  # Rotate every 60 seconds by default
        self.failed_proxies = set()  # Track failed proxies
    
    def add_proxy(self, proxy):
        """Add a proxy to the rotation list.
        
        Args:
            proxy (dict): A proxy dictionary with at least a 'server' key.
        """
        if isinstance(proxy, dict) and 'server' in proxy:
            self.proxies.append(proxy)
        else:
            raise ValueError("Proxy must be a dictionary with at least a 'server' key.")
    
    def remove_proxy(self, server):
        """Remove a proxy from the rotation list by its server address.
        
        Args:
            server (str): The server address of the proxy to remove.
        
        Returns:
            bool: True if the proxy was removed, False if not found.
        """
        for i, proxy in enumerate(self.proxies):
            if proxy['server'] == server:
                self.proxies.pop(i)
                return True
        return False
    
    def get_proxy(self, force_new=False):
        """Get a proxy configuration for use with Playwright.
        
        Args:
            force_new (bool, optional): Force a new proxy even if the rotation interval
                hasn't elapsed. Default is False.
        
        Returns:
            dict: A proxy configuration dictionary for Playwright, or None if no proxies are available.
        """
        if not self.proxies:
            return None
        
        # Check if we need to rotate the proxy
        current_time = time.time()
        if force_new or self.current_index == -1 or (current_time - self.last_rotation) > self.rotation_interval:
            # Get working proxies (exclude failed ones)
            working_proxies = [p for i, p in enumerate(self.proxies) 
                              if i not in self.failed_proxies]
            
            # If no working proxies, reset failed list and try all again
            if not working_proxies:
                self.failed_proxies = set()
                working_proxies = self.proxies
            
            # Select a random proxy
            if working_proxies:
                self.current_index = self.proxies.index(random.choice(working_proxies))
                self.last_rotation = current_time
        
        # Return the current proxy
        return self.proxies[self.current_index]
    
    def rotate_proxy(self):
        """Force a proxy rotation.
        
        Returns:
            dict: A new proxy configuration dictionary, or None if no proxies are available.
        """
        return self.get_proxy(force_new=True)
    
    def mark_proxy_failed(self):
        """Mark the current proxy as failed."""
        if self.current_index >= 0:
            self.failed_proxies.add(self.current_index)
    
    def reset_failed_proxies(self):
        """Reset the list of failed proxies."""
        self.failed_proxies = set()
    
    def set_rotation_interval(self, seconds):
        """Set the automatic proxy rotation interval.
        
        Args:
            seconds (int): Interval in seconds between automatic rotations.
        """
        self.rotation_interval = seconds
    
    def get_proxy_count(self):
        """Get the total number of proxies in the rotation.
        
        Returns:
            int: The number of proxies.
        """
        return len(self.proxies)
    
    def get_working_proxy_count(self):
        """Get the number of working proxies in the rotation.
        
        Returns:
            int: The number of working proxies.
        """
        return len(self.proxies) - len(self.failed_proxies)