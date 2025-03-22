# Playwright Web Scraper for Product Data

This script uses Playwright to automate a web browser, authenticate with a website, navigate through menus, and extract product data from tables with pagination.

## Requirements

- Python 3.7+
- Playwright

## Installation

1. Install the required packages:
```bash
pip install -r playwright_requirements.txt
```

2. Install Playwright browser dependencies:
```bash
python -m playwright install chromium
```

On Linux, you might need to install additional system dependencies. Playwright provides a convenient way to install them:
```bash
python -m playwright install-deps chromium
```

## Usage

Basic usage:
```bash
python playwright_scraper.py [options]
```

### Options

- `--username USERNAME`: Specify login username (default: "demo")
- `--password PASSWORD`: Specify login password (default: "password123")
- `--url URL`: Target website URL (default: http://localhost:5000)
- `--output FILENAME`: Output JSON file path (default: products_scraped.json)
- `--headless`: Run browser in headless mode (no UI)
- `--debug`: Enable detailed debug logging

### Examples

```bash
# Basic usage with default settings
python playwright_scraper.py

# With custom credentials and visible browser
python playwright_scraper.py --username admin --password secure123 --headless=False

# With custom URL and output file
python playwright_scraper.py --url https://example.com --output custom_data.json
```

## How it Works

1. The script launches a Chromium browser using Playwright
2. It navigates to the login page and authenticates with the provided credentials
3. It follows the navigation path: Menu → Data Management → Inventory → Products
4. On the products page, it extracts data from the table
5. If pagination exists, it navigates through all pages, collecting data
6. The collected data is processed and saved to a JSON file

## Advantages of Playwright

- Handles JavaScript-rendered content
- Automates complex user interactions
- Works with modern web applications
- Handles authentication and session management
- Supports multiple browsers (Chromium, Firefox, WebKit)
- Faster and more reliable than Selenium

## Troubleshooting

- **Browser not starting**: Make sure Playwright browsers are installed with `python -m playwright install`
- **Missing dependencies**: On Linux, run `python -m playwright install-deps chromium`
- **Authentication failures**: Check the username/password and verify the login form selectors
- **Navigation failures**: The website structure might have changed, requiring updates to the selectors