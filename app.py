from flask import Flask, request, jsonify, send_from_directory
import os
import sys
import glob
import logging

# Add the src directory to the path so we can import the modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.chromedriver import setup_driver, capture_with_retry
from src.paths import get_screenshot_path, assets_dir
from src.url_utils import format_url_to_filename

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('app')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    """Root endpoint, returns server status"""
    return jsonify({
        'status': 'online',
        'service': 'ChromeDriving',
        'endpoints': {
            '/submit-url': 'POST - Submit a URL for screenshot capture',
            '/screenshots': 'GET - List all available screenshots',
            '/screenshots/<filename>': 'GET - Retrieve a specific screenshot by filename',
            '/screenshots/by-url': 'GET - Retrieve screenshots for a specific URL (with url parameter)'
        }
    })

@app.route('/submit-url', methods=['POST'])
def submit_url():
    data = request.get_json()
    if not data or 'url' not in data:
        logger.warning('Request missing URL parameter')
        return jsonify({'error': 'URL is required'}), 400
    
    url = data['url']
    logger.info(f"Processing screenshot request for URL: {url}")
    
    try:
        # Capture screenshots with retry mechanism
        screenshot_files = capture_with_retry(url)
        
        # Prepare response with relative paths
        screenshots = []
        for file_path in screenshot_files:
            filename = os.path.basename(file_path)
            screenshots.append({
                'filename': filename,
                'path': f'/screenshots/{filename}'
            })
        
        logger.info(f"Successfully captured {len(screenshots)} screenshots for URL: {url}")
        return jsonify({
            'success': True, 
            'message': f'Captured {len(screenshots)} screenshots for URL: {url}',
            'url': url,
            'screenshots': screenshots
        })
    except ValueError as e:
        # Handle URL validation errors
        logger.error(f"URL validation error: {str(e)}")
        return jsonify({'error': f'Invalid URL: {str(e)}'}), 400
    except TimeoutError as e:
        # Handle timeout errors
        logger.error(f"Timeout error: {str(e)}")
        return jsonify({'error': f'Page load timeout: {str(e)}'}), 504
    except Exception as e:
        # Handle all other errors
        logger.error(f"Screenshot capture error: {str(e)}")
        return jsonify({'error': f'Failed to capture screenshot: {str(e)}'}), 500

@app.route('/screenshots', methods=['GET'])
def list_screenshots():
    """List all available screenshots"""
    try:
        # Get all PNG files in the assets directory
        screenshot_files = glob.glob(os.path.join(assets_dir, "*.png"))
        
        # Format the response with filenames
        screenshots = []
        for file in screenshot_files:
            filename = os.path.basename(file)
            screenshots.append({
                'filename': filename,
                'path': f'/screenshots/{filename}'
            })
            
        logger.info(f"Listed {len(screenshots)} screenshots")
        return jsonify({
            'success': True,
            'total': len(screenshots),
            'screenshots': screenshots
        })
    except Exception as e:
        logger.error(f"Failed to list screenshots: {str(e)}")
        return jsonify({'error': f'Failed to list screenshots: {str(e)}'}), 500

@app.route('/screenshots/<path:filename>', methods=['GET'])
def get_screenshot(filename):
    """Retrieve a specific screenshot by filename"""
    try:
        # Validate filename to prevent directory traversal
        if '..' in filename or filename.startswith('/'):
            logger.warning(f"Invalid filename requested: {filename}")
            return jsonify({'error': 'Invalid filename'}), 400
            
        file_path = os.path.join(assets_dir, filename)
        if not os.path.exists(file_path):
            logger.warning(f"Screenshot not found: {filename}")
            return jsonify({'error': 'Screenshot not found'}), 404
            
        logger.info(f"Serving screenshot: {filename}")
        return send_from_directory(assets_dir, filename)
    except Exception as e:
        logger.error(f"Error retrieving screenshot {filename}: {str(e)}")
        return jsonify({'error': f'Error retrieving screenshot: {str(e)}'}), 500

@app.route('/screenshots/by-url', methods=['GET'])
def get_screenshot_by_url():
    """Retrieve screenshots for a specific URL"""
    url = request.args.get('url')
    if not url:
        logger.warning("Request missing URL parameter")
        return jsonify({'error': 'URL parameter is required'}), 400
        
    try:
        # Get the filename pattern for this URL
        base_filename = format_url_to_filename(url)
        logger.info(f"Looking for screenshots for URL: {url} (base filename: {base_filename})")
        
        # The filename might have an index suffix if multiple screenshots were taken
        base_path = os.path.join(assets_dir, base_filename.replace('.png', ''))
        screenshot_files = glob.glob(f"{base_path}_*.png")
        
        # If no indexed files are found, try the direct filename
        if not screenshot_files:
            direct_path = os.path.join(assets_dir, base_filename)
            if os.path.exists(direct_path):
                screenshot_files = [direct_path]
        
        if not screenshot_files:
            logger.warning(f"No screenshots found for URL: {url}")
            return jsonify({
                'success': False,
                'error': 'No screenshots found for this URL',
                'url': url
            }), 404
            
        # Format the response
        screenshots = []
        for file in screenshot_files:
            filename = os.path.basename(file)
            screenshots.append({
                'filename': filename,
                'path': f'/screenshots/{filename}'
            })
            
        logger.info(f"Found {len(screenshots)} screenshots for URL: {url}")
        return jsonify({
            'success': True,
            'url': url,
            'total': len(screenshots),
            'screenshots': screenshots
        })
    except Exception as e:
        logger.error(f"Failed to retrieve screenshots for URL {url}: {str(e)}")
        return jsonify({'error': f'Failed to retrieve screenshots: {str(e)}'}), 500

if __name__ == '__main__':
    # Create assets directory if it doesn't exist
    os.makedirs(assets_dir, exist_ok=True)
    logger.info(f"Ensuring assets directory exists: {assets_dir}")
    
    # Log startup information
    logger.info("Starting ChromeDriving server")
    app.run(debug=True, host='0.0.0.0', port=5000) 