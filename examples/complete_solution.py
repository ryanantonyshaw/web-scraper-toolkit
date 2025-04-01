#!/usr/bin/env python3
"""
Complete Web Scraping Solution Example

This example demonstrates how to use all components of the web-scraper-toolkit together:
1. Stealth browser with anti-detection
2. Proxy rotation
3. CAPTCHA solving
4. Complete webpage saving

Usage:
    python complete_solution.py <url> <save_directory>

Example:
    python complete_solution.py https://example.com ./saved_pages

Requirements:
    - API keys for CAPTCHA solving service
    - Proxy credentials (if using proxy rotation)

These should be set in a .env file in the same directory as this script.
"""

import os
import sys
import time
import random
from dotenv import load_dotenv
from urllib.parse import urlparse

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import our modules
from playwright_stealth.stealth_browser import StealthBrowser
from captcha_solvers.anticaptcha import AntiCaptchaSolver
from proxy_handlers.smartproxy import SmartproxyRotator

# Load environment variables from .env file
load_dotenv()

def main():
    # Check command line arguments
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <url> [save_directory]")
        sys.exit(1)
    
    # Get URL from command line
    url = sys.argv[1]
    
    # Get save directory from command line or use default
    save_dir = sys.argv[2] if len(sys.argv) > 2 else './saved_pages'
    
    # Create save directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)
    
    # Get domain from URL for logging
    domain = urlparse(url).netloc
    
    print(f"\n{'=' * 50}")
    print(f"Starting web scraping for: {url}")
    print(f"{'=' * 50}\n")
    
    # Initialize proxy rotator if credentials are available
    proxy = None
    if os.getenv('SMARTPROXY_USERNAME') and os.getenv('SMARTPROXY_PASSWORD'):
        print("Setting up proxy rotation...")
        proxy_rotator = SmartproxyRotator(
            username=os.getenv('SMARTPROXY_USERNAME'),
            password=os.getenv('SMARTPROXY_PASSWORD'),
            endpoint=os.getenv('SMARTPROXY_ENDPOINT', 'gate.smartproxy.com'),
            port=int(os.getenv('SMARTPROXY_PORT', '7000'))
        )
        proxy = proxy_rotator.get_proxy()
        print(f"Using proxy: {proxy['server']}")
    else:
        print("No proxy credentials found. Running without proxy.")
    
    # Initialize CAPTCHA solver if API key is available
    captcha_solver = None
    if os.getenv('ANTICAPTCHA_API_KEY'):
        print("Setting up CAPTCHA solver...")
        captcha_solver = AntiCaptchaSolver(api_key=os.getenv('ANTICAPTCHA_API_KEY'))
        print("CAPTCHA solver ready")
    else:
        print("No CAPTCHA API key found. CAPTCHA solving will be skipped.")
    
    # Create a stealth browser
    print("\nStarting stealth browser...")
    browser = StealthBrowser(proxy=proxy, headless=False)  # Set headless=True for production
    
    # Navigate to the URL
    print(f"Navigating to {url}...")
    if not browser.navigate(url):
        print("Navigation failed. Exiting.")
        browser.close()
        sys.exit(1)
    
    # Check for CAPTCHA
    if browser.has_captcha():
        print("CAPTCHA detected!")
        
        if captcha_solver:
            print("Attempting to solve CAPTCHA...")
            site_key = browser.get_captcha_site_key()
            
            if site_key:
                print(f"Found CAPTCHA site key: {site_key}")
                solution = captcha_solver.solve_recaptcha(
                    website_url=url,
                    website_key=site_key
                )
                
                if solution:
                    print("CAPTCHA solved! Submitting solution...")
                    browser.submit_captcha_solution(solution)
                    print("Solution submitted. Waiting for page to load...")
                    time.sleep(5)  # Wait for page to load after CAPTCHA
                else:
                    print("Failed to solve CAPTCHA. Exiting.")
                    browser.close()
                    sys.exit(1)
            else:
                print("Could not find CAPTCHA site key. Exiting.")
                browser.close()
                sys.exit(1)
        else:
            print("No CAPTCHA solver available. Exiting.")
            browser.close()
            sys.exit(1)
    
    # Save the webpage
    print(f"\nSaving webpage to {save_dir}...")
    saved_path = browser.save_complete(save_dir)
    
    if saved_path:
        print(f"\nWebpage successfully saved to: {saved_path}")
        print(f"Resources saved to: {saved_path}_files/")
    else:
        print("Failed to save webpage.")
    
    # Take a screenshot for reference
    screenshot_path = os.path.join(save_dir, f"{domain}_{int(time.time())}.png")
    browser.screenshot(screenshot_path)
    print(f"Screenshot saved to: {screenshot_path}")
    
    # Close the browser
    print("\nClosing browser...")
    browser.close()
    
    print(f"\n{'=' * 50}")
    print(f"Web scraping completed for: {url}")
    print(f"{'=' * 50}\n")

if __name__ == "__main__":
    main()