from urllib.parse import urlparse, unquote
import re
import logging

logger = logging.getLogger('url_utils')

def validate_url(url):
    """
    Validates and normalizes a URL.
    
    Args:
        url (str): The URL to validate
        
    Returns:
        str: The normalized URL
        
    Raises:
        ValueError: If URL is invalid
    """
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")
        
    # Trim whitespace
    url = url.strip()
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = f"http://{url}"
    
    try:
        parsed = urlparse(url)
        if not parsed.netloc:
            raise ValueError(f"Invalid URL format: {url}")
    except Exception as e:
        logger.error(f"URL parse error: {str(e)}")
        raise ValueError(f"Invalid URL: {str(e)}")
        
    return url

def format_url_to_filename(url):
    """
    Formats a URL into a safe filename.
    
    Args:
        url (str): The URL to format
        
    Returns:
        str: A filename-safe representation of the URL
    """
    try:
        # Validate and normalize URL
        url = validate_url(url)
        
        # Parse URL components
        parsed_url = urlparse(url)
        
        # Extract domain without www.
        domain = parsed_url.netloc
        if domain.startswith('www.'):
            domain = domain[4:]
            
        # Clean up domain (replace invalid characters)
        domain = re.sub(r'[^a-zA-Z0-9.-]', '_', domain)
        
        # Extract and clean path
        path = parsed_url.path.strip('/')
        
        # URL decode the path (handle special characters)
        path = unquote(path)
        
        # Replace path separators and invalid characters
        path = re.sub(r'[^a-zA-Z0-9.-]', '_', path)
        
        # Truncate if too long (preventing extremely long filenames)
        if len(path) > 100:
            path = path[:100]
            
        # Build filename
        if path:
            filename = f"{domain}_{path}.png"
        else:
            filename = f"{domain}.png"
            
        # Ensure no double underscores
        filename = re.sub(r'_+', '_', filename)
        
        logger.debug(f"Formatted URL {url} to filename {filename}")
        return filename
        
    except Exception as e:
        logger.error(f"Error formatting URL to filename: {str(e)}")
        # Provide a fallback for error cases
        safe_url = re.sub(r'[^a-zA-Z0-9.-]', '_', url)
        return f"error_{safe_url[:50]}.png"