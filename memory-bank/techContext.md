# Technical Context

## Technologies Used

- **Python**: Core programming language for the project
- **Flask**: Web framework for building the server application
- **Selenium**: Browser automation library for capturing screenshots
- **Chrome WebDriver**: Chrome-specific driver for Selenium
- **WebDriver Manager**: Tool for managing WebDriver binaries
- **PDF2Image**: Library for converting PDFs to images
- **PyTesseract**: Python wrapper for Tesseract OCR engine
- **Pillow (PIL)**: Python Imaging Library for image processing
- **Tesseract**: OCR engine for extracting text from images
- **Poppler**: PDF rendering library
- **Docker**: Containerization platform for packaging the application
- **Xvfb**: Virtual framebuffer for running Chrome in headless mode

## Development Setup

### Prerequisites

- Python 3.x
- Google Chrome browser
- Tesseract OCR engine (installed via brew on macOS)
- Poppler (installed via brew on macOS)
- Docker (optional, for containerized deployment)

### Installation

```bash
# Install system dependencies (macOS)
brew update && brew install tesseract poppler

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

- Relies on system-level dependencies (Tesseract, Poppler, Chrome)
- Screenshot capabilities dependent on Chrome browser availability
- OCR accuracy dependent on image quality and Tesseract's capabilities
- WebDriver needs to be compatible with the installed Chrome version
- Docker containers need proper permissions for file system access

## Dependencies

- **Core Dependencies**:
  - Flask: Web server framework
  - selenium: Browser automation for screenshots
  - webdriver-manager: Manages WebDriver installation
  - pdf2image: For PDF to image conversion if needed
  - pytesseract: For OCR functionality
  - Pillow: For image manipulation
- **System Dependencies**:
  - Chrome browser: For rendering web pages
  - tesseract: OCR engine
  - poppler: PDF rendering
  - xvfb: Virtual framebuffer (for Docker deployment)

## Tool Usage Patterns

- **Flask**: Used for creating the web server and API endpoints
- **Selenium**: Used for browser automation and screenshot capture
- **Chrome WebDriver**: Drives the Chrome browser for Selenium
- **Tesseract**: Used for extracting text from captured screenshots
- **PDF2Image**: May be used for handling PDF content from web pages
- **Pillow**: Used for image preprocessing, format conversion, and manipulations
- **Docker**: Used for containerizing the application for easy deployment
- **Xvfb**: Used for running Chrome in headless mode in the Docker container
