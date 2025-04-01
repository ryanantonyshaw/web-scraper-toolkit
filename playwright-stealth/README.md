# Playwright-Stealth Core

This directory contains the core web scraping solution using Playwright with stealth capabilities.

## What's Included

- `stealth_browser.py` - Main browser class with anti-detection features
- `fingerprint_manager.py` - Tools to manage and rotate browser fingerprints
- `page_saver.py` - Functions to save complete webpages (HTML, CSS, JS)
- `utils.py` - Helper utilities

## How It Works

The core solution uses Playwright to automate Chrome/Chromium with various anti-detection techniques:

1. TLS fingerprint spoofing
2. WebRTC prevention
3. Canvas noise injection
4. AudioContext masking
5. Font fingerprint randomization

It can save complete webpages exactly as Chrome would with 'Save as webpage complete'.

## Usage Example

```python
from stealth_browser import StealthBrowser

# Create a stealth browser instance
browser = StealthBrowser()

# Navigate to a website
browser.navigate('https://example.com')

# Save the complete webpage
browser.save_complete('example_site')

# Close the browser
browser.close()
```