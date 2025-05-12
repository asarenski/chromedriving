# Active Context

## Current Focus

The project is in its implementation stage. The core focus areas are:

- Building out the server functionality (completed)
- Implementing URL submission endpoint (completed)
- Implementing screenshot capture functionality (completed)
- Establishing storage mechanisms for screenshots (basic implementation completed)
- Adding functionality to retrieve captured screenshots (completed)
- Implementing error handling improvements for screenshot capture edge cases (completed)
- Creating Docker containerization (completed)
- Transitioning from Google Chrome to Chromium
- Integrating OCR capabilities

## Recent Changes

- Created the project repository
- Added basic README with setup instructions
- Identified core dependencies (pdf2image, pytesseract, Pillow, tesseract, poppler)
- Created Flask application with basic structure
- Implemented `/submit-url` endpoint for URL submission via POST requests
- Integrated screenshot capture functionality using Selenium ChromeDriver
- Added file-based storage for screenshots in the assets directory
- Added endpoints to retrieve screenshots:
  - `/screenshots` - lists all available screenshots
  - `/screenshots/<filename>` - retrieves a specific screenshot by filename
  - `/screenshots/by-url?url=<url>` - retrieves screenshots for a specific URL
- Implemented comprehensive error handling for screenshot capture:
  - Added URL validation and formatting improvements
  - Implemented retry mechanism for failed screenshot attempts
  - Enhanced cookie banner handling with more robust detection
  - Added logging for better troubleshooting
  - Added specific error types for different failure scenarios
  - Improved response structure with clearer error messages
  - Added security validations for file access
- Created a Makefile with commands for building and running the application:
  - Added setup, run, and clean commands
  - Added development and production mode options
  - Added screenshot management commands
  - Added Docker integration commands
- Added Docker support for containerization:
  - Created Dockerfile with all necessary dependencies (Chrome, Tesseract, Poppler)
  - Configured appropriate permissions and non-root user for security
  - Updated Makefile with Docker commands (build, run, stop)
  - Added .dockerignore file to optimize Docker build

## Next Steps

1. ~~Create a Dockerfile so the service can be run in docker.~~ (Completed)
2. ~~Create a Makefile so build and run commands are easy.~~ (Completed)
3. Setup the project to use Chromium instead of Google Chrome.
4. Implement OCR capabilities using Tesseract.

## Active Decisions

- Selected Selenium as the browser automation tool
- Using file system for screenshot storage (organized by domain and path)
- Enhanced error handling approach with retry mechanism, specific exception handling, and comprehensive logging
- Structure for processing pipeline to be determined
- Added RESTful endpoints for screenshot retrieval with multiple access methods
- Created Makefile for simplified build and run commands
- Using Docker for containerized deployment with all dependencies
- Planning to transition from Google Chrome to Chromium

## Important Patterns and Preferences

- Using Flask for the web server implementation
- JSON-based API for request/response handling
- Selenium for browser automation and screenshot capture
- File-based storage with organized naming conventions
- Preference for modular design to allow easy extension of processing capabilities
- Emphasis on robust error handling for production-quality operation
- Focus on simplicity for initial implementation
- RESTful API design for resource access
- Comprehensive logging for debugging and monitoring
- Containerized deployment for consistency across environments

## Learnings and Project Insights

- Initial research indicates Tesseract works best with high-quality images
- PDF processing may require specific handling for different types of documents
- Flask provides a simple but powerful framework for our server implementation
- Selenium effectively handles screenshot capture with automated cookie banner handling
- Robust error handling is essential for dealing with the unpredictable nature of web pages
- Retry mechanisms are important for handling transient failures in web interactions
- URL validation and normalization is critical for handling user input reliably
- Containerization simplifies deployment and ensures consistent dependencies
- Xvfb is necessary for running Chrome in headless mode in a Docker container
