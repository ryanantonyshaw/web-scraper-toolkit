import os
import re
import time
import shutil
from urllib.parse import urlparse, urljoin

def save_page_complete(page, save_path):
    """Save a webpage completely (HTML, CSS, JS) using Chrome's 'Save as...' functionality.
    
    Args:
        page: The Playwright page object.
        save_path (str): Directory path where to save the webpage.
    
    Returns:
        str: Path to the saved HTML file, or None if saving failed.
    """
    try:
        # Create the save directory if it doesn't exist
        os.makedirs(save_path, exist_ok=True)
        
        # Get the page URL and title
        url = page.url
        title = page.title()
        
        # Create a sanitized filename from the title
        filename = sanitize_filename(title) + '.html'
        full_path = os.path.join(save_path, filename)
        
        # Create a resources directory for assets
        resources_dir = os.path.join(save_path, filename + '_files')
        os.makedirs(resources_dir, exist_ok=True)
        
        # Get the HTML content
        html_content = page.content()
        
        # Save all resources (images, CSS, JS)
        html_content = download_resources(page, html_content, resources_dir, url)
        
        # Save the HTML file
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Webpage saved to: {full_path}")
        return full_path
    
    except Exception as e:
        print(f"Error saving page: {e}")
        return None

def sanitize_filename(filename):
    """Sanitize a string to be used as a filename.
    
    Args:
        filename (str): The string to sanitize.
    
    Returns:
        str: A sanitized filename.
    """
    # Replace invalid characters with underscores
    sanitized = re.sub(r'[\\/*?:"<>|]', '_', filename)
    # Limit length
    if len(sanitized) > 100:
        sanitized = sanitized[:97] + '...'
    # Ensure we have at least something
    if not sanitized or sanitized.isspace():
        sanitized = 'webpage'
    return sanitized

def download_resources(page, html_content, resources_dir, base_url):
    """Download all resources referenced in the HTML and update the references.
    
    Args:
        page: The Playwright page object.
        html_content (str): The HTML content.
        resources_dir (str): Directory to save resources.
        base_url (str): The base URL of the page.
    
    Returns:
        str: Updated HTML content with local references.
    """
    # Extract and download CSS files
    css_pattern = re.compile(r'<link[^>]*?href=["\']([^"\'>]*?\.css[^"\'>]*?)["\'][^>]*?>', re.IGNORECASE)
    for match in css_pattern.finditer(html_content):
        css_url = match.group(1)
        absolute_url = urljoin(base_url, css_url)
        local_path = download_resource(page, absolute_url, resources_dir)
        if local_path:
            rel_path = os.path.relpath(local_path, os.path.dirname(resources_dir))
            html_content = html_content.replace(css_url, rel_path)
    
    # Extract and download JavaScript files
    js_pattern = re.compile(r'<script[^>]*?src=["\']([^"\'>]*?\.js[^"\'>]*?)["\'][^>]*?>', re.IGNORECASE)
    for match in js_pattern.finditer(html_content):
        js_url = match.group(1)
        absolute_url = urljoin(base_url, js_url)
        local_path = download_resource(page, absolute_url, resources_dir)
        if local_path:
            rel_path = os.path.relpath(local_path, os.path.dirname(resources_dir))
            html_content = html_content.replace(js_url, rel_path)
    
    # Extract and download images
    img_pattern = re.compile(r'<img[^>]*?src=["\']([^"\'>]*?)["\'][^>]*?>', re.IGNORECASE)
    for match in img_pattern.finditer(html_content):
        img_url = match.group(1)
        absolute_url = urljoin(base_url, img_url)
        local_path = download_resource(page, absolute_url, resources_dir)
        if local_path:
            rel_path = os.path.relpath(local_path, os.path.dirname(resources_dir))
            html_content = html_content.replace(img_url, rel_path)
    
    return html_content

def download_resource(page, url, resources_dir):
    """Download a single resource.
    
    Args:
        page: The Playwright page object.
        url (str): URL of the resource to download.
        resources_dir (str): Directory to save the resource.
    
    Returns:
        str: Local path to the saved resource, or None if download failed.
    """
    try:
        # Parse the URL to get the filename
        parsed_url = urlparse(url)
        path = parsed_url.path
        filename = os.path.basename(path)
        
        # If no filename or extension, generate one
        if not filename or '.' not in filename:
            extension = guess_extension(url)
            filename = f"resource_{int(time.time())}_{hash(url) % 10000}{extension}"
        
        # Create a sanitized filename
        filename = sanitize_filename(filename)
        
        # Full path to save the resource
        save_path = os.path.join(resources_dir, filename)
        
        # Create subdirectories if needed
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Download the resource using Playwright
        with page.context.new_page() as resource_page:
            try:
                response = resource_page.goto(url, timeout=10000)
                if response and response.ok:
                    content = response.body()
                    with open(save_path, 'wb') as f:
                        f.write(content)
                    return save_path
            except Exception as e:
                print(f"Error downloading resource {url}: {e}")
        
        return None
    
    except Exception as e:
        print(f"Error processing resource {url}: {e}")
        return None

def guess_extension(url):
    """Guess the file extension based on the URL.
    
    Args:
        url (str): The URL to analyze.
    
    Returns:
        str: The guessed file extension including the dot.
    """
    # Check for common extensions in the URL
    if re.search(r'\.js(\?|$)', url, re.IGNORECASE):
        return '.js'
    elif re.search(r'\.css(\?|$)', url, re.IGNORECASE):
        return '.css'
    elif re.search(r'\.(jpg|jpeg)(\?|$)', url, re.IGNORECASE):
        return '.jpg'
    elif re.search(r'\.png(\?|$)', url, re.IGNORECASE):
        return '.png'
    elif re.search(r'\.gif(\?|$)', url, re.IGNORECASE):
        return '.gif'
    elif re.search(r'\.svg(\?|$)', url, re.IGNORECASE):
        return '.svg'
    elif re.search(r'\.webp(\?|$)', url, re.IGNORECASE):
        return '.webp'
    elif re.search(r'\.woff2?(\?|$)', url, re.IGNORECASE):
        return '.woff'
    elif re.search(r'\.ttf(\?|$)', url, re.IGNORECASE):
        return '.ttf'
    elif re.search(r'\.eot(\?|$)', url, re.IGNORECASE):
        return '.eot'
    
    # Default to .bin for unknown types
    return '.bin'