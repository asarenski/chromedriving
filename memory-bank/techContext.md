# Technical Context

## Technologies Used

- **Python**: Core programming language for the project
- **Flask**: Web framework for building the server application
- **Selenium**: Browser automation library for capturing screenshots
- **Chromium**: Open-source browser for rendering web pages
- **ChromeDriver**: Chromium-specific driver for Selenium
- **WebDriver Manager**: Tool for managing WebDriver binaries
- **PDF2Image**: Library for converting PDFs to images
- **PyTesseract**: Python wrapper for Tesseract OCR engine
- **Pillow (PIL)**: Python Imaging Library for image processing
- **Tesseract**: OCR engine for extracting text from images
- **Poppler**: PDF rendering library
- **Docker**: Containerization platform for packaging the application
- **Xvfb**: Virtual framebuffer for running Chromium in headless mode

## Development Setup

### Prerequisites

- Python 3.x
- Chromium browser (or Google Chrome on macOS)
- Tesseract OCR engine (installed via brew on macOS, apt on Linux)
- Poppler (installed via brew on macOS, apt on Linux)
- Docker (optional, for containerized deployment)

### Installation

```bash
# Install system dependencies (macOS)
brew update && brew install tesseract poppler

# Install system dependencies (Linux/Debian)
apt-get update && apt-get install -y tesseract-ocr poppler-utils chromium chromium-driver

# Install Python dependencies
pip install Flask selenium webdriver-manager pdf2image pytesseract Pillow
```

### Docker Setup

For containerized deployment:

```bash
# Build Docker image
make docker-build

# Run Docker container
make docker-run
```

## Technical Constraints

- Relies on system-level dependencies (Tesseract, Poppler, Chromium/Chrome)
- Screenshot capabilities dependent on Chromium/Chrome browser availability
- OCR accuracy dependent on image quality and Tesseract's capabilities
- ChromeDriver needs to be compatible with the installed Chromium/Chrome version
- Platform-specific configurations required for different operating systems
- Docker containers need proper permissions for file system access and ChromeDriver execution

## Dependencies

- **Core Dependencies**:
  - Flask: Web server framework
  - selenium: Browser automation for screenshots
  - webdriver-manager: Manages WebDriver installation
  - pdf2image: For PDF to image conversion if needed
  - pytesseract: For OCR functionality
  - Pillow: For image manipulation
- **System Dependencies**:
  - Chromium browser: For rendering web pages (preferred, especially in Docker)
  - Chrome browser: Alternative for macOS and Windows environments
  - ChromeDriver: WebDriver for Chromium/Chrome
  - tesseract: OCR engine
  - poppler: PDF rendering
  - xvfb: Virtual framebuffer (for Docker deployment)

## Tool Usage Patterns

- **Flask**: Used for creating the web server and API endpoints
- **Selenium**: Used for browser automation and screenshot capture
- **Chromium/ChromeDriver**: Used for rendering web pages and capturing screenshots
- **Tesseract**: Used for extracting text from captured screenshots
- **PDF2Image**: May be used for handling PDF content from web pages
- **Pillow**: Used for image preprocessing, format conversion, and manipulations
- **Docker**: Used for containerizing the application for easy deployment
- **Xvfb**: Used for running Chromium in headless mode in the Docker container

## Environment-Specific Configurations

- **MacOS**:

  - Uses local Chrome or Chromium browser
  - ChromeDriver managed via WebDriver Manager
  - System dependencies installed via Homebrew

- **Linux/Docker**:
  - Uses Chromium from system packages
  - Uses ChromeDriver from system packages
  - System dependencies installed via apt-get
  - Runs browser in headless mode via Xvfb
