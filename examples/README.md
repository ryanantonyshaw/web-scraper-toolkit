# Examples

This directory contains complete working examples for different web scraping scenarios.

## Available Examples

- `basic_scraper.py` - Simple example of downloading a webpage
- `captcha_handling.py` - Example with CAPTCHA solving
- `proxy_rotation.py` - Example with proxy rotation
- `complete_solution.py` - Full example with all features

## Complete Solution Example

The `complete_solution.py` file demonstrates how to use all components together:

1. Stealth browser with anti-detection
2. Proxy rotation
3. CAPTCHA solving
4. Complete webpage saving

```python
# Import the necessary components
from playwright_stealth import StealthBrowser
from captcha_solvers.anticaptcha import AntiCaptchaSolver
from proxy_handlers.smartproxy import SmartproxyRotator

# Set up proxy rotation
proxy_rotator = SmartproxyRotator(
    username='YOUR_USERNAME',
    password='YOUR_PASSWORD'
)

# Set up CAPTCHA solving
captcha_solver = AntiCaptchaSolver(api_key='YOUR_API_KEY')

# Create a stealth browser with proxy
proxy = proxy_rotator.get_proxy()
browser = StealthBrowser(proxy=proxy)

# Navigate to a website
browser.navigate('https://example.com')

# Check for CAPTCHA and solve if needed
if browser.has_captcha():
    site_key = browser.get_captcha_site_key()
    solution = captcha_solver.solve_recaptcha(
        website_url='https://example.com',
        website_key=site_key
    )
    browser.submit_captcha_solution(solution)

# Save the complete webpage
browser.save_complete('example_site')

# Close the browser
browser.close()
```