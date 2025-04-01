import os
import random
import time
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

from .fingerprint_manager import get_random_fingerprint
from .page_saver import save_page_complete
from .utils import detect_captcha, extract_captcha_sitekey

class StealthBrowser:
    """A browser class with anti-detection features for web scraping."""
    
    def __init__(self, proxy=None, headless=False):
        """Initialize a new stealth browser instance.
        
        Args:
            proxy (dict, optional): Proxy configuration for the browser.
                Format: {'server': 'http://proxy.example.com:8080', 'username': 'user', 'password': 'pass'}
            headless (bool, optional): Whether to run the browser in headless mode. Default is False.
        """
        self.proxy = proxy
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self._start_browser()
    
    def _start_browser(self):
        """Start the browser with stealth settings."""
        self.playwright = sync_playwright().start()
        
        # Get a random fingerprint for the browser
        fingerprint = get_random_fingerprint()
        
        # Launch browser with proxy if provided
        launch_args = {
            'headless': self.headless,
            'args': [
                '--disable-blink-features=AutomationControlled',
                '--disable-features=IsolateOrigins,site-per-process',
                f'--user-agent={fingerprint["user_agent"]}'
            ]
        }
        
        if self.proxy:
            launch_args['proxy'] = self.proxy
        
        self.browser = self.playwright.chromium.launch(**launch_args)
        
        # Create a context with the fingerprint
        self.context = self.browser.new_context(
            viewport=fingerprint['viewport'],
            device_scale_factor=fingerprint['device_scale_factor'],
            locale=fingerprint['locale'],
            timezone_id=fingerprint['timezone_id'],
            color_scheme=fingerprint['color_scheme'],
            reduced_motion='reduce' if fingerprint['reduced_motion'] else 'no-preference',
            has_touch=fingerprint['has_touch']
        )
        
        # Apply stealth mode
        stealth_sync(self.context)
        
        # Create a new page
        self.page = self.context.new_page()
        
        # Add random delays to common methods to appear more human-like
        self._add_human_behavior()
    
    def _add_human_behavior(self):
        """Add random delays and human-like behavior to the browser."""
        # Store original methods
        original_click = self.page.click
        original_fill = self.page.fill
        original_press = self.page.press
        original_goto = self.page.goto
        
        # Override methods with delayed versions
        def delayed_click(*args, **kwargs):
            time.sleep(random.uniform(0.1, 0.5))
            return original_click(*args, **kwargs)
        
        def delayed_fill(*args, **kwargs):
            time.sleep(random.uniform(0.1, 0.3))
            return original_fill(*args, **kwargs)
        
        def delayed_press(*args, **kwargs):
            time.sleep(random.uniform(0.05, 0.2))
            return original_press(*args, **kwargs)
        
        def delayed_goto(*args, **kwargs):
            time.sleep(random.uniform(0.5, 1.5))
            return original_goto(*args, **kwargs)
        
        # Replace methods
        self.page.click = delayed_click
        self.page.fill = delayed_fill
        self.page.press = delayed_press
        self.page.goto = delayed_goto
    
    def navigate(self, url, wait_until='networkidle', timeout=30000):
        """Navigate to a URL.
        
        Args:
            url (str): The URL to navigate to.
            wait_until (str, optional): When to consider navigation finished.
                Options: 'domcontentloaded', 'load', 'networkidle'. Default is 'networkidle'.
            timeout (int, optional): Maximum navigation time in milliseconds. Default is 30000.
        
        Returns:
            bool: True if navigation was successful, False otherwise.
        """
        try:
            self.page.goto(url, wait_until=wait_until, timeout=timeout)
            # Scroll down slowly to trigger lazy loading
            self._scroll_page()
            return True
        except Exception as e:
            print(f"Navigation error: {e}")
            return False
    
    def _scroll_page(self, scroll_delay=100):
        """Scroll the page to trigger lazy loading.
        
        Args:
            scroll_delay (int, optional): Delay between scroll steps in milliseconds. Default is 100.
        """
        self.page.evaluate("""
        () => {
            return new Promise((resolve) => {
                let totalHeight = 0;
                const distance = 100;
                const timer = setInterval(() => {
                    const scrollHeight = document.body.scrollHeight;
                    window.scrollBy(0, distance);
                    totalHeight += distance;
                    
                    if(totalHeight >= scrollHeight){
                        clearInterval(timer);
                        resolve();
                    }
                }, %s);
            });
        }
        """ % scroll_delay)
    
    def has_captcha(self):
        """Check if the current page has a CAPTCHA.
        
        Returns:
            bool: True if a CAPTCHA is detected, False otherwise.
        """
        return detect_captcha(self.page)
    
    def get_captcha_site_key(self):
        """Extract the CAPTCHA site key from the current page.
        
        Returns:
            str: The CAPTCHA site key if found, None otherwise.
        """
        return extract_captcha_sitekey(self.page)
    
    def submit_captcha_solution(self, solution):
        """Submit a CAPTCHA solution to the current page.
        
        Args:
            solution (str): The CAPTCHA solution.
        
        Returns:
            bool: True if submission was successful, False otherwise.
        """
        try:
            # Insert the solution into the g-recaptcha-response textarea
            self.page.evaluate(f"""
            (solution) => {{
                document.getElementById('g-recaptcha-response').innerHTML = solution;
                // Try to trigger the form submission
                const forms = document.querySelectorAll('form');
                if (forms.length > 0) {{
                    forms[0].submit();
                }}
            }}
            """, solution)
            
            # Wait for navigation after form submission
            self.page.wait_for_navigation()
            return True
        except Exception as e:
            print(f"CAPTCHA submission error: {e}")
            return False
    
    def save_complete(self, save_path):
        """Save the current page as a complete webpage (HTML, CSS, JS).
        
        Args:
            save_path (str): Directory path where to save the webpage.
        
        Returns:
            str: Path to the saved HTML file, or None if saving failed.
        """
        return save_page_complete(self.page, save_path)
    
    def screenshot(self, path):
        """Take a screenshot of the current page.
        
        Args:
            path (str): Path where to save the screenshot.
        
        Returns:
            bool: True if screenshot was saved successfully, False otherwise.
        """
        try:
            self.page.screenshot(path=path, full_page=True)
            return True
        except Exception as e:
            print(f"Screenshot error: {e}")
            return False
    
    def close(self):
        """Close the browser and all associated resources."""
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()