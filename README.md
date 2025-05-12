# ChromeDriving

A server application that allows users to input URLs and capture screenshots of web pages for later processing. The screenshots can be stored and processed for various purposes.

## Features

- Submit URLs for screenshot capture
- Store screenshots in organized file system
- Retrieve captured screenshots via various endpoints
- Comprehensive error handling with retry mechanisms
- Automated cookie banner handling

## Prerequisites

- Python 3.x
- Google Chrome browser
- Tesseract OCR engine (for OCR functionality)
- Poppler (for PDF processing)

## Setup and Installation

1. Install system dependencies (macOS):

   ```bash
   brew update && brew install tesseract poppler
   ```

2. Setup the Python environment:

   ```bash
   make setup
   ```

   Or manually:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Using the Makefile:

```bash
make run
```

Or manually:

```bash
python app.py
```

The server will start on port 5001. Access the API at:

```
http://localhost:5001/
```

## Running with Docker

### Building the Docker Image

```bash
make docker-build
```

Or manually:

```bash
docker build -t chromedriving:latest .
```

### Running the Docker Container

```bash
make docker-run
```

Or manually:

```bash
docker run -d -p 5001:5001 --name chromedriving-container chromedriving:latest
```

### Stopping the Docker Container

```bash
make docker-stop
```

Or manually:

```bash
docker stop chromedriving-container
docker rm chromedriving-container
```

## Available Makefile Commands

Use `make help` to see all available commands:

- `make setup` - Install dependencies and prepare environment
- `make run` - Run the Flask application
- `make run-prod` - Run in production mode
- `make debug` - Run in debug mode
- `make clean` - Clean up generated files
- `make clean-screenshots` - Remove all captured screenshots
- `make lint` - Run linting checks
- `make test` - Run tests (when implemented)
- `make docker-build` - Build Docker image
- `make docker-run` - Run Docker container
- `make docker-stop` - Stop Docker container

## API Endpoints

- `GET /` - Server status and API documentation
- `POST /submit-url` - Submit a URL for screenshot capture
- `GET /screenshots` - List all available screenshots
- `GET /screenshots/<filename>` - Retrieve a specific screenshot by filename
- `GET /screenshots/by-url?url=<url>` - Retrieve screenshots for a specific URL

## Project Structure

- `app.py`: Main Flask application file
- `src/`: Source code directory
  - `chromedriver.py`: Selenium-based screenshot capture engine
  - `url_utils.py`: URL handling utilities
  - `paths.py`: Path management utilities
- `assets/`: Directory for storing captured screenshots
- `requirements.txt`: Dependencies for the project
- `Makefile`: Build and run commands
- `Dockerfile`: Docker container configuration
