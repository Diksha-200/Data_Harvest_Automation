# Web Scraper for Product Data

A Python-based web scraper that authenticates with a web application, navigates through menus, and extracts product data from tables with pagination support.

## Features

- Authentication with username/password
- Session management
- HTML-based or API-based data extraction
- Pagination handling
- Data export to JSON
- Detailed logging
- Command-line interface with flexible parameters

## Requirements

- Python 3.7+
- Required packages:
  - requests
  - beautifulsoup4

## Installation

1. Download the project files
2. Install the required packages:

```bash
pip install -r project_requirements.txt
```

## Usage

Basic usage:

```bash
python requests_scraper.py [options]
```

### Options

- `--api`: Use the API-based method instead of HTML parsing (faster and more reliable)
- `--username USERNAME`: Specify login username (default: "demo")
- `--password PASSWORD`: Specify login password (default: "password123") 
- `--url URL`: Target website URL (default: http://0.0.0.0:5000)
- `--output FILENAME`: Output JSON file path (default: products_scraped.json)
- `--debug`: Enable detailed debug logging

### Examples

```bash
# Use API-based scraping with default credentials
python requests_scraper.py --api

# HTML-based scraping with custom credentials
python requests_scraper.py --username admin --password secure123

# API-based scraping with debug logs and custom output file
python requests_scraper.py --api --debug --output products_data.json
```

## Using with a Different Website

To use this scraper with a different website:

1. Update the target URL with the `--url` parameter
2. Provide appropriate login credentials with `--username` and `--password`
3. You may need to modify the following parts of the code for the specific website:
   - Login form field selectors
   - Navigation path and link selectors
   - Table structure and data extraction logic

## Project Structure

- `requests_scraper.py`: Main script with HTML and API-based scrapers
- `project_requirements.txt`: List of required Python packages