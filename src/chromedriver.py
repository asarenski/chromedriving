import os
import sys
import time
import logging
import platform
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import (
    WebDriverException, 
    TimeoutException, 
    NoSuchElementException, 
    ElementNotInteractableException,
    InvalidArgumentException,
    StaleElementReferenceException,
    JavascriptException
)
from webdriver_manager.chrome import ChromeDriverManager

from src.paths import assets_dir, get_screenshot_path
from src.url_utils import format_url_to_filename

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('chromedriver')

# Constants
MAX_RETRIES = 3
RETRY_DELAY = 2
PAGE_LOAD_TIMEOUT = 30
SCROLL_HEIGHT = 1080
WAIT_TIME_COOKIE = 3
WAIT_TIME_CSS = 1
SCROLL_PAUSE_TIME = 0.5

def validate_url(url):
    """
    Validates if the URL is properly formatted and includes a scheme.
    Returns the validated URL or raises ValueError.
    """
    try:
        parsed = urlparse(url)
        if not parsed.scheme:
            # Add http:// if no scheme is provided
            url = f"http://{url}"
            parsed = urlparse(url)
        
        if not parsed.netloc:
            raise ValueError(f"Invalid URL: {url}")
            
        return url
    except Exception as e:
        raise ValueError(f"URL validation error: {str(e)}")

def setup_driver():
    """
    Sets up and returns a Chrome WebDriver with appropriate options.
    Handles potential setup failures and adapts to the operating system.
    """
    try:
        options = Options()
        options.add_argument('--headless=new')  # Updated headless mode
        options.add_argument(f'--window-size=1920,{SCROLL_HEIGHT}')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--disable-logging')
        
        # Add platform-specific configuration
        system = platform.system()
        logger.info(f"Setting up Chrome driver on {system} platform")
        
        if system == "Darwin":  # macOS
            # Common Chrome locations on macOS
            chrome_paths = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Chromium.app/Contents/MacOS/Chromium"
            ]
            
            chrome_found = False
            for path in chrome_paths:
                if os.path.exists(path):
                    options.binary_location = path
                    logger.info(f"Using Chrome binary at: {path}")
                    chrome_found = True
                    break
            
            if not chrome_found:
                logger.warning("Chrome binary not found in standard locations. Using default.")
        elif system == "Linux":  # Linux/Docker
            # Check for Chromium
            chromium_path = "/usr/bin/chromium"
            if os.path.exists(chromium_path):
                options.binary_location = chromium_path
                logger.info(f"Using Chromium binary at: {chromium_path}")
            else:
                logger.warning("Chromium binary not found at expected location")
        
        # Check for system ChromeDriver
        system_chromedriver = "/usr/bin/chromedriver"
        if os.path.exists(system_chromedriver):
            logger.info(f"Using system ChromeDriver at {system_chromedriver}")
            # Log permissions and executable status for debugging
            try:
                import stat
                st = os.stat(system_chromedriver)
                logger.info(f"ChromeDriver permissions: {stat.filemode(st.st_mode)}")
                logger.info(f"ChromeDriver is executable: {os.access(system_chromedriver, os.X_OK)}")
            except Exception as e:
                logger.warning(f"Failed to check ChromeDriver permissions: {e}")
                
            # Create the service with appropriate permissions
            service = Service(executable_path=system_chromedriver)
            
            # Set up driver with version-appropriate configuration
            try:
                logger.info("Starting Chrome with system ChromeDriver")
                driver = webdriver.Chrome(service=service, options=options)
            except Exception as e:
                logger.error(f"Failed to start Chrome with system ChromeDriver: {e}")
                # If it fails, try different permissions
                try:
                    logger.info("Attempting to run ChromeDriver with sudo")
                    # This is a fallback that will likely fail in Docker, but it's worth a try
                    import subprocess
                    subprocess.run(["chmod", "a+x", system_chromedriver])
                    driver = webdriver.Chrome(service=service, options=options)
                except Exception as e2:
                    logger.error(f"All attempts to start ChromeDriver failed: {e2}")
                    raise RuntimeError(f"Unable to start ChromeDriver after multiple attempts: {e2}")
        else:
            # Try auto-installation as fallback
            logger.warning("System ChromeDriver not found, using WebDriver Manager")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        
        return driver
    except WebDriverException as e:
        logger.error(f"Failed to setup Chrome driver: {str(e)}")
        raise RuntimeError(f"Chrome driver setup failed: {str(e)}")

def decline_cookies_if_present(driver):
    """
    Attempts to find and click a 'Decline All' or 'Reject All' cookie button if present.
    Tries common button texts and aria-labels.
    """
    button_texts = [
        'Decline All', 'Reject All', 'Deny All', 'Only Essential', 'Decline', 'Reject', 'Deny',
        'Use necessary only', 'Use essential only', 'Refuse', 'Disagree'
    ]
    
    try:
        # Try by button text
        for text in button_texts:
            try:
                # Try exact match
                button = driver.find_element('xpath', f"//button[normalize-space(text())='{text}']")
                button.click()
                logger.info(f"Clicked cookie button with text: {text}")
                return True
            except (NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException):
                pass
            try:
                # Try contains (case-insensitive)
                button = driver.find_element('xpath', f"//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text.lower()}')]")
                button.click()
                logger.info(f"Clicked cookie button containing text: {text}")
                return True
            except (NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException):
                pass
                
        # Try by aria-label
        for text in button_texts:
            try:
                button = driver.find_element('xpath', f"//button[contains(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text.lower()}')]")
                button.click()
                logger.info(f"Clicked cookie button with aria-label containing: {text}")
                return True
            except (NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException):
                pass
                
        # Try input[type=button|submit] with value
        for text in button_texts:
            try:
                button = driver.find_element('xpath', f"//input[(translate(@value, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='{text.lower()}') and (@type='button' or @type='submit')]")
                button.click()
                logger.info(f"Clicked cookie input button with value: {text}")
                return True
            except (NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException):
                pass
                
        # Try generic cookie consent selectors
        try:
            # Common cookie consent IDs
            id_patterns = ['cookie-consent', 'cookieConsent', 'cookie-banner', 'cookieBanner', 'gdpr-banner']
            for id_pattern in id_patterns:
                try:
                    element = driver.find_element('css selector', f"#*{id_pattern}* button")
                    element.click()
                    logger.info(f"Clicked button in element with ID containing: {id_pattern}")
                    return True
                except (NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException):
                    pass
        except Exception:
            pass
            
        logger.info("No cookie banner detected or unable to decline cookies")
        return False
        
    except Exception as e:
        logger.warning(f"Error handling cookie consent: {str(e)}")
        return False

def inject_screenshot_css(driver):
    """
    Injects CSS to remove hover/focus effects for cleaner screenshots.
    """
    try:
        driver.execute_script("""
            var style = document.createElement('style');
            style.innerHTML = `
                * {
                    pointer-events: none !important;
                    user-select: none !important;
                }
                *:hover, *:focus, *:active {
                    background-color: inherit !important;
                    color: inherit !important;
                    border-color: inherit !important;
                    outline: none !important;
                    box-shadow: none !important;
                    transform: none !important;
                    opacity: 1 !important;
                }
            `;
            document.head.appendChild(style);
        """)
        logger.debug("Injected screenshot CSS")
        return True
    except JavascriptException as e:
        logger.warning(f"Failed to inject CSS: {str(e)}")
        return False

def take_screenshot(driver, path, scroll_position=0):
    """
    Takes a screenshot at the specified scroll position.
    Returns True if successful, False otherwise.
    """
    try:
        # Scroll to the current position
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        time.sleep(SCROLL_PAUSE_TIME)
        
        # Save screenshot
        driver.save_screenshot(path)
        logger.debug(f"Screenshot saved: {path}")
        return True
    except Exception as e:
        logger.error(f"Failed to take screenshot at position {scroll_position}: {str(e)}")
        return False

def get_url_screenshot(driver, url, retry_count=0):
    """
    Captures screenshots of the URL with scrolling.
    Includes retry mechanism and better error handling.
    """
    try:
        # Validate and normalize URL
        validated_url = validate_url(url)
        logger.info(f"Getting screenshot for URL: {validated_url}")
        
        # Navigate to the URL
        driver.get(validated_url)
        
        # Wait for page to load
        time.sleep(WAIT_TIME_COOKIE)
        
        # Try to decline cookies
        decline_cookies_if_present(driver)
        
        # Wait for cookie banner to disappear
        time.sleep(WAIT_TIME_CSS)
        
        # Remove hover/focus effects by injecting CSS
        inject_screenshot_css(driver)
        
        # Get page height
        total_height = int(driver.execute_script("return document.body.scrollHeight"))
        logger.info(f"Page height: {total_height}px")
        
        # Take screenshots
        screenshot_index = 0
        current_scroll = 0
        screenshots = []
        
        while current_scroll < total_height:
            # Generate screenshot path
            screenshot_path = get_screenshot_path(url).replace('.png', f'_{screenshot_index}.png')
            
            # Take screenshot
            if take_screenshot(driver, screenshot_path, current_scroll):
                screenshots.append(screenshot_path)
                screenshot_index += 1
            
            # Increment scroll position
            current_scroll += SCROLL_HEIGHT
            
            # Update total_height in case the page grows
            try:
                new_height = int(driver.execute_script("return document.body.scrollHeight"))
                if new_height > total_height:
                    logger.info(f"Page height increased from {total_height}px to {new_height}px")
                    total_height = new_height
            except JavascriptException as e:
                logger.warning(f"Failed to update page height: {str(e)}")
        
        logger.info(f"Captured {len(screenshots)} screenshots for URL: {url}")
        return screenshots
        
    except TimeoutException as e:
        logger.warning(f"Page load timeout for URL {url}: {str(e)}")
        if retry_count < MAX_RETRIES:
            logger.info(f"Retrying (attempt {retry_count + 1}/{MAX_RETRIES})...")
            time.sleep(RETRY_DELAY)
            return get_url_screenshot(driver, url, retry_count + 1)
        else:
            logger.error(f"Max retries exceeded for URL: {url}")
            raise TimeoutException(f"Page load timeout after {MAX_RETRIES} retries: {str(e)}")
            
    except InvalidArgumentException as e:
        logger.error(f"Invalid URL argument: {url}")
        raise ValueError(f"Invalid URL format: {str(e)}")
        
    except WebDriverException as e:
        logger.error(f"WebDriver error for URL {url}: {str(e)}")
        if retry_count < MAX_RETRIES:
            logger.info(f"Retrying (attempt {retry_count + 1}/{MAX_RETRIES})...")
            time.sleep(RETRY_DELAY)
            # Restart driver for serious errors
            driver.quit()
            driver = setup_driver()
            return get_url_screenshot(driver, url, retry_count + 1)
        else:
            logger.error(f"Max retries exceeded for URL: {url}")
            raise WebDriverException(f"WebDriver error after {MAX_RETRIES} retries: {str(e)}")
            
    except Exception as e:
        logger.error(f"Unexpected error capturing screenshot for URL {url}: {str(e)}")
        raise
        
    finally:
        # Don't quit the driver here as it might be reused in retry attempts
        pass

def capture_with_retry(url, max_retries=MAX_RETRIES):
    """
    Wrapper function to set up driver and capture screenshots with retry logic.
    """
    driver = None
    retry_count = 0
    
    while retry_count <= max_retries:
        try:
            if driver is None:
                driver = setup_driver()
            
            screenshots = get_url_screenshot(driver, url, retry_count)
            return screenshots
            
        except (TimeoutException, WebDriverException) as e:
            retry_count += 1
            logger.warning(f"Attempt {retry_count}/{max_retries} failed: {str(e)}")
            
            if retry_count <= max_retries:
                logger.info(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
                
                # For WebDriver issues, recreate the driver
                if isinstance(e, WebDriverException) and driver is not None:
                    try:
                        driver.quit()
                    except:
                        pass
                    driver = None
            else:
                logger.error(f"All {max_retries} retry attempts failed")
                raise
                
        except Exception as e:
            logger.error(f"Fatal error: {str(e)}")
            raise
            
        finally:
            # Clean up driver in the final iteration or on fatal error
            if retry_count > max_retries and driver is not None:
                try:
                    driver.quit()
                except:
                    pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chromedriver.py <url>")
        sys.exit(1)
    url = sys.argv[1]
    try:
        screenshots = capture_with_retry(url)
        print(f"Successfully captured {len(screenshots)} screenshots")
        for screenshot in screenshots:
            print(f" - {screenshot}")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
