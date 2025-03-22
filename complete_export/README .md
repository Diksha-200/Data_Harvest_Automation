# Web Scraper Demo Project

This package contains both:
1. A demo website with product data
2. Playwright-based web scraper to extract data from the website

## Project Structure

```
complete_export/
├── website/           # Flask demo website
│   ├── app.py         # Main Flask application
│   ├── main.py        # Entry point to run the website
│   └── *.html         # HTML templates
├── scraper/           # Web scraper implementations
│   ├── playwright_scraper.py      # Playwright-based scraper (recommended)
│   ├── playwright_requirements.txt # Playwright dependencies
│   ├── requests_scraper.py        # Alternative requests-based scraper
│   └── project_requirements.txt   # Alternative scraper dependencies
```

## Running the Demo Website

1. Install requirements:
```bash
pip install flask flask-sqlalchemy
```

2. Navigate to the website directory:
```bash
cd website
```

3. Run the Flask application:
```bash
python main.py
```

The website will be available at http://localhost:5000

## Demo Website Credentials
- Username: `demo`
- Password: `password123`

## Running the Playwright Scraper (Recommended)

Playwright offers a powerful browser automation solution that handles JavaScript rendering and complex interactions.

1. Install Playwright requirements:
```bash
cd scraper
pip install -r playwright_requirements.txt
python -m playwright install chromium
```

2. On Linux systems, install additional system dependencies:
```bash
python -m playwright install-deps chromium
```

3. Run the Playwright scraper:
```bash
# Headless mode (no visible browser)
python playwright_scraper.py --url http://localhost:5000

# To see the browser in action
python playwright_scraper.py --url http://localhost:5000 --headless=False
```

The scraper will:
1. Log in to the website with the demo credentials
2. Navigate through menus to the products page
3. Extract all product data, handling pagination
4. Save the data to `products_scraped.json`

## Advantages of the Playwright Scraper

- Handles JavaScript-rendered content
- Automates complex user interactions
- Works with modern web applications
- Takes screenshots for debugging when errors occur
- Compatible with multiple browsers (Chromium, Firefox, WebKit)
- More robust for handling complex websites

## Notes

- Make sure the website is running before executing the scraper
- Use the `--debug` flag for detailed logging
- The website simulates a product management system with test data
- The scraped data is stored in JSON format suitable for further processing