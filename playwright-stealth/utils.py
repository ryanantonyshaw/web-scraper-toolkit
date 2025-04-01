import re

def detect_captcha(page):
    """Detect if a page contains a CAPTCHA.
    
    Args:
        page: The Playwright page object.
    
    Returns:
        bool: True if a CAPTCHA is detected, False otherwise.
    """
    # Check for common CAPTCHA elements
    captcha_selectors = [
        # reCAPTCHA v2
        '.g-recaptcha',
        'iframe[src*="recaptcha"]',
        'iframe[src*="google.com/recaptcha"]',
        # reCAPTCHA v3
        'script[src*="recaptcha"]',
        # hCaptcha
        '.h-captcha',
        'iframe[src*="hcaptcha.com"]',
        # Arkose Labs (FunCaptcha)
        'iframe[src*="arkoselabs.com"]',
        'iframe[src*="funcaptcha"]',
        # Cloudflare Turnstile
        '.cf-turnstile',
        'iframe[src*="challenges.cloudflare.com"]',
        # General CAPTCHA keywords
        '[id*="captcha"]',
        '[class*="captcha"]',
        '[name*="captcha"]',
    ]
    
    # Check for each selector
    for selector in captcha_selectors:
        try:
            if page.query_selector(selector):
                return True
        except:
            pass
    
    # Check for CAPTCHA keywords in the page content
    content = page.content().lower()
    captcha_keywords = ['captcha', 'robot check', 'human verification', 'security check']
    for keyword in captcha_keywords:
        if keyword in content:
            return True
    
    return False

def extract_captcha_sitekey(page):
    """Extract the CAPTCHA site key from the page.
    
    Args:
        page: The Playwright page object.
    
    Returns:
        str: The CAPTCHA site key if found, None otherwise.
    """
    # Try to extract reCAPTCHA site key
    try:
        # Method 1: From g-recaptcha div data-sitekey attribute
        recaptcha_element = page.query_selector('.g-recaptcha')
        if recaptcha_element:
            site_key = recaptcha_element.get_attribute('data-sitekey')
            if site_key:
                return site_key
        
        # Method 2: From script content
        content = page.content()
        site_key_match = re.search(r'["\']sitekey["\']\s*:\s*["\']([\w-]+)["\']', content)
        if site_key_match:
            return site_key_match.group(1)
        
        # Method 3: From recaptcha/api.js URL
        site_key_match = re.search(r'google\.com/recaptcha/api\.js\?render=([\w-]+)', content)
        if site_key_match:
            return site_key_match.group(1)
        
        # Method 4: From explicit render call
        site_key_match = re.search(r'grecaptcha\.render\(.*?["\']([\w-]+)["\']', content)
        if site_key_match:
            return site_key_match.group(1)
    except Exception as e:
        print(f"Error extracting reCAPTCHA site key: {e}")
    
    # Try to extract hCaptcha site key
    try:
        hcaptcha_element = page.query_selector('.h-captcha')
        if hcaptcha_element:
            site_key = hcaptcha_element.get_attribute('data-sitekey')
            if site_key:
                return site_key
    except Exception as e:
        print(f"Error extracting hCaptcha site key: {e}")
    
    # Try to extract Turnstile site key
    try:
        turnstile_element = page.query_selector('.cf-turnstile')
        if turnstile_element:
            site_key = turnstile_element.get_attribute('data-sitekey')
            if site_key:
                return site_key
    except Exception as e:
        print(f"Error extracting Turnstile site key: {e}")
    
    return None

def extract_domain(url):
    """Extract the domain from a URL.
    
    Args:
        url (str): The URL to extract the domain from.
    
    Returns:
        str: The domain name.
    """
    match = re.search(r'https?://(?:www\.)?([^/]+)', url)
    if match:
        return match.group(1)
    return url

def is_headless_detected(page):
    """Check if the page can detect that the browser is running in headless mode.
    
    Args:
        page: The Playwright page object.
    
    Returns:
        bool: True if headless mode is detected, False otherwise.
    """
    # Run a series of tests that websites commonly use to detect headless browsers
    detection_script = """
    () => {
        const tests = {
            // Check if navigator.webdriver is defined
            'webdriver': !!navigator.webdriver,
            
            // Check for Chrome properties that are missing in headless
            'chrome': {
                'app': typeof chrome === 'undefined' || typeof chrome.app === 'undefined',
                'runtime': typeof chrome === 'undefined' || typeof chrome.runtime === 'undefined'
            },
            
            // Check for inconsistencies in navigator properties
            'navigator': {
                'plugins': navigator.plugins.length === 0,
                'languages': navigator.languages.length === 0,
                'permissions': typeof navigator.permissions === 'undefined'
            },
            
            // Check for automation-specific behavior
            'automation': {
                'connection': navigator.connection === undefined,
                'touchpoints': navigator.maxTouchPoints === 0
            }
        };
        
        // Count how many tests failed (indicating headless detection)
        let failedTests = 0;
        let totalTests = 0;
        
        const countFailures = (obj) => {
            for (const key in obj) {
                if (typeof obj[key] === 'object') {
                    countFailures(obj[key]);
                } else {
                    totalTests++;
                    if (obj[key] === true) {
                        failedTests++;
                    }
                }
            }
        };
        
        countFailures(tests);
        
        // Return true if more than 30% of tests failed
        return {
            detected: failedTests / totalTests > 0.3,
            failedTests,
            totalTests,
            details: tests
        };
    }
    """
    
    result = page.evaluate(detection_script)
    return result.get('detected', False)