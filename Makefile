# Makefile for ChromeDriving Project

.PHONY: help setup run clean lint test docker-build docker-run docker-stop

# Variables
PYTHON := python3
PIP := pip3
APP := app.py
PORT := 5001
HOST := 0.0.0.0
DOCKER_IMAGE := chromedriving
DOCKER_TAG := latest
DOCKER_CONTAINER := chromedriving-container

help: ## Show available commands
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Install dependencies and prepare the environment
	@echo "Installing dependencies..."
	$(PIP) install -r requirements.txt
	@mkdir -p assets
	@echo "Checking system dependencies..."
	@which chromedriver || echo "WARNING: chromedriver not found. Selenium will attempt to download it."
	@which tesseract || echo "WARNING: tesseract not found. OCR functionality will not work."
	@which pdftoppm || echo "WARNING: pdftoppm (poppler) not found. PDF processing will not work."
	@echo "Setup complete"

run: ## Run the Flask application
	@echo "Starting ChromeDriving server..."
	$(PYTHON) $(APP)

run-prod: ## Run the Flask application in production mode
	@echo "Starting ChromeDriving server in production mode..."
	FLASK_ENV=production $(PYTHON) $(APP)

debug: ## Run the Flask application in debug mode
	@echo "Starting ChromeDriving server in debug mode..."
	FLASK_ENV=development FLASK_DEBUG=1 $(PYTHON) $(APP)

clean: ## Clean generated files and cached Python files
	@echo "Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".tox" -exec rm -rf {} +
	@echo "Cleanup complete"

clean-screenshots: ## Remove all captured screenshots
	@echo "Removing all screenshots..."
	rm -rf assets/*.png
	@echo "Screenshots removed"

lint: ## Run linting checks
	@echo "Running linters..."
	@which pylint > /dev/null || echo "pylint not installed, skipping"
	@which pylint > /dev/null && pylint src/ app.py || echo "pylint check failed"
	@which flake8 > /dev/null || echo "flake8 not installed, skipping"
	@which flake8 > /dev/null && flake8 src/ app.py || echo "flake8 check failed"
	@echo "Linting complete"

test: ## Run tests
	@echo "Running tests..."
	@echo "No tests configured yet"
	@echo "Tests complete"

# Docker commands
docker-build: ## Build Docker image
	@echo "Building Docker image..."
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .

docker-run: ## Run Docker container
	@echo "Running Docker container..."
	docker run -d -p $(PORT):$(PORT) --name $(DOCKER_CONTAINER) $(DOCKER_IMAGE):$(DOCKER_TAG)

docker-stop: ## Stop Docker container
	@echo "Stopping Docker container..."
	docker stop $(DOCKER_CONTAINER) || true
	docker rm $(DOCKER_CONTAINER) || true 