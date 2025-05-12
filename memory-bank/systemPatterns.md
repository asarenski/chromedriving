# System Patterns

## Architecture Overview

ChromeDriving is designed as a server application with the following components:

- Flask web server for handling URL submission requests
- Selenium-based screenshot capture engine
- File system storage for the captured screenshots
- Processing pipeline for applying operations to the screenshots (including OCR)
- Docker container for consistent deployment

## Design Patterns

- **REST API Pattern**: Server provides RESTful endpoints for URL submission and resource management
- **Client-Server Pattern**: Server accepts URL requests and returns/stores screenshot results
- **Pipeline Pattern**: For processing screenshots through various stages (capture, preprocessing, OCR, etc.)
- **Repository Pattern**: For organized storage and retrieval of captured screenshots
- **Strategy Pattern**: For handling different screenshot capture approaches based on page content
- **Container Pattern**: Docker containerization for encapsulation and consistent deployment

## Component Relationships

```
[Client] → [Flask Web Server] → [Selenium Screenshot Engine] → [File Storage]
                                       ↓
                               [Processing Pipeline]
                                       ↓
                             [Processed Results Storage]
```

## Docker Deployment Architecture

```
[Host Machine] → [Docker Container] → [Flask App + Dependencies]
                        ↓
                [Xvfb + Chrome] → [Screenshot Capture]
                        ↓
                [Volume Mount] → [Persistent Storage]
```

## Screenshot Capture Flow

```
[URL Submitted] → [Initialize Chrome] → [Load Page] → [Handle Cookies] → [Scroll & Capture] → [Store Screenshots]
```

## API Design

- **`/`**: Root endpoint, basic server status (GET)
- **`/submit-url`**: Accept URL for screenshot capture (POST)
  - Input: JSON with URL parameter
  - Output: Success/failure status with screenshot information
- **`/screenshots`**: List all available screenshots (GET)
  - Output: List of screenshot filenames and their access paths
- **`/screenshots/<filename>`**: Retrieve a specific screenshot by filename (GET)
  - Output: The screenshot image file
- **`/screenshots/by-url`**: Retrieve screenshots for a specific URL (GET)
  - Input: URL as a query parameter
  - Output: List of screenshot filenames and their access paths for the specified URL

## Critical Implementation Paths

1. **URL Submission**: Client submits URL to server via `/submit-url` endpoint
2. **Screenshot Capture**: Server uses Selenium ChromeDriver to navigate to URL and capture screenshot
   - Includes cookie banner handling
   - Scrolling mechanism for full-page capture
3. **Storage**: Screenshots are saved to the assets directory with organized names
4. **Retrieval**: Screenshots can be listed and accessed via various endpoints
5. **Processing**: Optional processing steps (like OCR) are applied
6. **Result Delivery**: Screenshot information or error message is returned to client

## Technical Decisions

- Using Python for server implementation
- Flask for web server framework
- JSON for API request/response format
- Selenium for browser automation and screenshot capture
- File system for organized screenshot storage
- RESTful API design for resource access
- Tesseract for OCR capabilities (planned)
- PDF tools for potential PDF processing
- Pillow for image manipulation
- Docker for containerized deployment
- Non-root user in Docker for security
- Xvfb for headless browser operation in container
