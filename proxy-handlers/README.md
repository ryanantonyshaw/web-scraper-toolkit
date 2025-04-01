# Proxy Handlers

This directory contains proxy rotation and management tools for web scraping.

## Supported Proxy Services

- Smartproxy (recommended)
- Bright Data (formerly Luminati)
- IPRoyal
- Custom proxy lists

## How to Use

### Smartproxy Integration

```python
from proxy_handlers.smartproxy import SmartproxyRotator

# Create a proxy rotator
proxy_rotator = SmartproxyRotator(
    username='YOUR_USERNAME',
    password='YOUR_PASSWORD',
    endpoint='gate.smartproxy.com',
    port=7000
)

# Get a proxy for use with Playwright
proxy = proxy_rotator.get_proxy()
print(f"Using proxy: {proxy['server']}")

# Use in Playwright
browser = playwright.chromium.launch(proxy=proxy)
```

### Custom Proxy List

```python
from proxy_handlers.custom import CustomProxyRotator

# Create a list of proxies
proxies = [
    {'server': 'http://proxy1.example.com:8080', 'username': 'user1', 'password': 'pass1'},
    {'server': 'http://proxy2.example.com:8080', 'username': 'user2', 'password': 'pass2'},
]

# Create a proxy rotator
proxy_rotator = CustomProxyRotator(proxies=proxies)

# Get a proxy
proxy = proxy_rotator.get_proxy()
```

## Pricing

### Smartproxy
- Starting at $12/month
- Pay-as-you-go option at $6/GB

### Bright Data
- Residential proxies start at $499/month ($6.43/GB)
- Pay-as-you-go at $8.4/GB

### IPRoyal
- Starting at $4.55/GB with volume discounts
- No monthly plans - buy traffic as needed