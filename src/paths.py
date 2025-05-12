import os
from .url_utils import format_url_to_filename

# Determine the assets directory path relative to this script's location
assets_dir = os.path.join(os.path.dirname(__file__), '..', 'assets')

def get_screenshot_path(url):
    os.makedirs(assets_dir, exist_ok=True)
    return os.path.join(assets_dir, format_url_to_filename(url))

if __name__ == "__main__":
    print(assets_dir) 