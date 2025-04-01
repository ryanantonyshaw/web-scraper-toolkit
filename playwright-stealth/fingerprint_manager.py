import random
import json
import os
from datetime import datetime

# Common user agents
USER_AGENTS = [
    # Chrome on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    # Chrome on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    # Firefox on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    # Firefox on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
    # Safari on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    # Edge on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
]

# Common viewport sizes
VIEWPORTS = [
    {'width': 1920, 'height': 1080},  # Full HD
    {'width': 1680, 'height': 1050},  # Common desktop
    {'width': 1440, 'height': 900},   # Common laptop
    {'width': 1366, 'height': 768},   # Common laptop
    {'width': 1280, 'height': 800},   # Common laptop
    {'width': 1280, 'height': 720},   # HD
]

# Common device scale factors
DEVICE_SCALE_FACTORS = [1, 1.5, 2]

# Common locales
LOCALES = ['en-US', 'en-GB', 'en-CA', 'en-AU', 'fr-FR', 'de-DE', 'es-ES', 'it-IT']

# Common timezones
TIMEZONES = [
    'America/New_York',
    'America/Los_Angeles',
    'America/Chicago',
    'Europe/London',
    'Europe/Paris',
    'Europe/Berlin',
    'Asia/Tokyo',
    'Asia/Singapore',
    'Australia/Sydney',
]

# Color schemes
COLOR_SCHEMES = ['light', 'dark', 'no-preference']

def get_random_fingerprint():
    """Generate a random browser fingerprint.
    
    Returns:
        dict: A dictionary containing random fingerprint values.
    """
    return {
        'user_agent': random.choice(USER_AGENTS),
        'viewport': random.choice(VIEWPORTS),
        'device_scale_factor': random.choice(DEVICE_SCALE_FACTORS),
        'locale': random.choice(LOCALES),
        'timezone_id': random.choice(TIMEZONES),
        'color_scheme': random.choice(COLOR_SCHEMES),
        'reduced_motion': random.choice([True, False]),
        'has_touch': random.choice([True, False, False, False]),  # Less likely to have touch
    }

def load_fingerprints(file_path):
    """Load fingerprints from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file containing fingerprints.
    
    Returns:
        list: A list of fingerprint dictionaries.
    """
    if not os.path.exists(file_path):
        return []
    
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading fingerprints: {e}")
        return []

def save_fingerprints(fingerprints, file_path):
    """Save fingerprints to a JSON file.
    
    Args:
        fingerprints (list): A list of fingerprint dictionaries.
        file_path (str): Path where to save the fingerprints.
    
    Returns:
        bool: True if saving was successful, False otherwise.
    """
    try:
        with open(file_path, 'w') as f:
            json.dump(fingerprints, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving fingerprints: {e}")
        return False

def get_fingerprint_for_domain(domain, fingerprints_file='fingerprints.json'):
    """Get a consistent fingerprint for a specific domain.
    
    This helps maintain the same fingerprint when visiting the same domain multiple times,
    which can help avoid detection.
    
    Args:
        domain (str): The domain to get a fingerprint for.
        fingerprints_file (str, optional): Path to the fingerprints file. Default is 'fingerprints.json'.
    
    Returns:
        dict: A fingerprint dictionary for the domain.
    """
    fingerprints = load_fingerprints(fingerprints_file)
    
    # Check if we already have a fingerprint for this domain
    for fp in fingerprints:
        if fp.get('domain') == domain:
            return fp
    
    # Create a new fingerprint for this domain
    new_fingerprint = get_random_fingerprint()
    new_fingerprint['domain'] = domain
    new_fingerprint['created_at'] = datetime.now().isoformat()
    
    # Save the updated fingerprints
    fingerprints.append(new_fingerprint)
    save_fingerprints(fingerprints, fingerprints_file)
    
    return new_fingerprint