#!/usr/bin/env python3
"""
Playwright-based Web Scraper

This script uses Playwright to automate a web browser, authenticate with a website,
navigate through menus, and extract product data from tables, handling pagination.
"""
import argparse
import json
import logging
import os
import time
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PlaywrightProductScraper:
    """
    A class to scrape product data using Playwright browser automation.
    
    This scraper authenticates with the web application, navigates through menus,
    and extracts product data from tables, handling pagination.
    """
    
    def __init__(
        self, 
        base_url: str, 
        username: str, 
        password: str,
        headless: bool = True
    ):
        """
        Initialize the PlaywrightProductScraper.
        
        Args:
            base_url: The base URL of the web application
            username: Username for authentication
            password: Password for authentication
            headless: Whether to run the browser in headless mode
        """
        self.base_url = base_url
        self.username = username
        self.password = password
        self.headless = headless
        self.page = None
        self.browser = None
        self.playwright = None
        
    def run(self) -> List[Dict[str, Any]]:
        """
        Execute the scraping process.
        
        Returns:
            A list of dictionaries containing product data
        """
        try:
            logger.info(f"Starting Playwright scraper for {self.base_url}")
            
            # Initialize Playwright
            self._initialize()
            
            # Navigate to the login page
            logger.info(f"Navigating to {self.base_url}")
            self.page.goto(self.base_url)
            
            # Perform login
            self._login()
            
            # Navigate to the products page
            self._navigate_to_products_page()
            
            # Extract product data
            products = self._extract_product_data()
            
            logger.info(f"Extracted {len(products)} products")
            return products
            
        except Exception as e:
            logger.error(f"Error during scraping: {str(e)}")
            # Take a screenshot for debugging
            if self.page:
                self.page.screenshot(path="error_screenshot.png")
            raise
        finally:
            self.cleanup()
    
    def _initialize(self):
        """Initialize Playwright, browser, and context."""
        from playwright.sync_api import sync_playwright
        
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.page = self.browser.new_page()
        
        # Set default timeout
        self.page.set_default_timeout(10000)  # 10 seconds
    
    def _login(self):
        """
        Perform login with provided credentials.
        """
        logger.info(f"Logging in to {self.base_url} with username: {self.username}")
        
        # Check if we're already on the login page, if not navigate to it
        if "/login" not in self.page.url:
            self.page.goto(f"{self.base_url}/login")
        
        # Fill in login form
        self.page.fill('input[name="username"]', self.username)
        self.page.fill('input[name="password"]', self.password)
        
        # Click login button
        self.page.click('button[type="submit"]')
        
        # Wait for navigation to complete
        self.page.wait_for_load_state("networkidle")
        
        # Verify login success
        if not self._is_authenticated():
            logger.error("Login failed. Check credentials or website structure.")
            raise Exception("Failed to login")
        
        logger.info("Login successful")
    
    def _is_authenticated(self) -> bool:
        """
        Check if the current session is authenticated.
        
        Returns:
            True if authenticated, False otherwise
        """
        # Check for the presence of logout link or user-specific element
        try:
            # Wait briefly for the page to stabilize
            time.sleep(1)
            
            # The URL usually changes after login to a dashboard or home page
            current_url = self.page.url
            if "/login" in current_url:
                return False
            
            # Check for elements that are typically present after login
            # This could be a logout link, user profile, or dashboard elements
            has_menu = self.page.query_selector('a:text("Menu")') is not None
            has_logout = self.page.query_selector('a:text("Logout")') is not None
            
            return has_menu or has_logout
            
        except Exception as e:
            logger.error(f"Error checking authentication: {str(e)}")
            return False
    
    def _navigate_to_products_page(self):
        """
        Navigate through the application to the products page.
        
        Path: Menu -> Data Management -> Inventory -> Products
        """
        logger.info("Navigating to products page")
        
        # Click on "Menu"
        self._click_with_retry('a:text("Menu")', "Menu link")
        
        # Click on "Data Management"
        self._click_with_retry('a:text("Data Management")', "Data Management link")
        
        # Click on "Inventory"
        self._click_with_retry('a:text("Inventory")', "Inventory link")
        
        # Click on "Products"
        self._click_with_retry('a:text("Products")', "Products link")
        
        # Wait for the products table to load
        self.page.wait_for_selector('table', state='visible')
        
        logger.info("Successfully navigated to products page")
    
    def _click_with_retry(self, selector: str, element_name: str, retries: int = 3):
        """
        Attempt to click an element with retries.
        
        Args:
            selector: CSS selector for the element
            element_name: Name of the element for logging
            retries: Number of retry attempts
        """
        for attempt in range(retries):
            try:
                # Wait for element to be visible
                self.page.wait_for_selector(selector, state='visible')
                
                # Click the element
                self.page.click(selector)
                
                # Wait for navigation or loading to complete
                self.page.wait_for_load_state("networkidle")
                
                return  # Success, exit function
            except Exception as e:
                if attempt < retries - 1:
                    logger.warning(f"Attempt {attempt+1}/{retries} to click {element_name} failed: {str(e)}. Retrying...")
                    time.sleep(1)  # Wait before retrying
                else:
                    logger.error(f"Failed to click {element_name} after {retries} attempts")
                    raise
    
    def _extract_product_data(self) -> List[Dict[str, Any]]:
        """
        Extract product data from the table, handling pagination.
        
        Returns:
            List of dictionaries containing product data
        """
        all_products = []
        page_num = 1
        max_pages = 20  # Safety limit
        
        while page_num <= max_pages:
            logger.info(f"Extracting data from page {page_num}")
            
            # Wait for the table to be fully loaded
            self.page.wait_for_selector('table', state='visible')
            
            # Extract headers
            header_columns = self._extract_table_headers()
            
            # Extract products from current page
            page_products = self._extract_products_from_current_page(header_columns)
            all_products.extend(page_products)
            
            # Check if there is a next page
            if not self._go_to_next_page():
                break
            
            page_num += 1
            
            # Safety check
            if page_num > max_pages:
                logger.warning(f"Reached max page limit of {max_pages}")
                break
        
        return all_products
    
    def _extract_table_headers(self) -> List[str]:
        """
        Extract table header columns.
        
        Returns:
            List of header column names
        """
        headers = self.page.query_selector_all('table thead th')
        header_columns = [header.inner_text().strip() for header in headers]
        return header_columns
    
    def _extract_products_from_current_page(self, header_columns: List[str]) -> List[Dict[str, Any]]:
        """
        Extract product data from the current page.
        
        Args:
            header_columns: List of header column names
            
        Returns:
            List of dictionaries, each representing a product
        """
        products = []
        
        # Get all rows excluding the header row
        rows = self.page.query_selector_all('table tbody tr')
        
        for row in rows:
            # Get all cells in the row
            cells = row.query_selector_all('td')
            
            # Skip rows with inappropriate number of cells
            if len(cells) != len(header_columns):
                continue
            
            # Create a dictionary with header names as keys
            product = {}
            for i, header in enumerate(header_columns):
                # Skip the "Actions" column
                if header == "Actions":
                    continue
                
                cell_text = cells[i].inner_text().strip()
                
                # Convert values to appropriate types
                if header == "ID":
                    product["id"] = int(cell_text)
                elif header == "Price":
                    # Remove currency symbol and convert to float
                    product["price"] = float(cell_text.replace("$", "").strip())
                elif header == "Stock":
                    product["stock"] = int(cell_text)
                elif header == "Name":
                    product["name"] = cell_text
                elif header == "Category":
                    product["category"] = cell_text
            
            products.append(product)
        
        return products
    
    def _go_to_next_page(self) -> bool:
        """
        Attempt to navigate to the next page if pagination exists.
        
        Returns:
            True if successfully navigated to next page, False if no more pages
        """
        try:
            # Look for the "Next" link in the pagination
            next_link = self.page.query_selector('a:text("Next")')
            
            # If there's no Next link or it's disabled, we're on the last page
            if not next_link or "disabled" in (next_link.get_attribute("class") or ""):
                logger.info("No more pages available")
                return False
            
            # Click on the Next link
            next_link.click()
            
            # Wait for the page to load
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_selector('table', state='visible')
            
            # Verify we're on a different page
            logger.info("Navigated to next page")
            return True
            
        except Exception as e:
            logger.error(f"Error navigating to next page: {str(e)}")
            return False
    
    def _save_screenshot(self, filename: str):
        """
        Save a screenshot for debugging purposes.
        
        Args:
            filename: Name of the screenshot file
        """
        if self.page:
            self.page.screenshot(path=filename)
            logger.info(f"Screenshot saved as {filename}")
    
    def cleanup(self):
        """Clean up resources."""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Playwright-based web scraper for product data")
    parser.add_argument("--username", default="demo", help="Username for login")
    parser.add_argument("--password", default="password123", help="Password for login")
    parser.add_argument("--url", default="http://localhost:5000", help="Base URL of the web application")
    parser.add_argument("--output", default="products_scraped.json", help="Output JSON file path")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    
    return parser.parse_args()


def main():
    """Main function to run the scraper."""
    args = parse_arguments()
    
    # Set debug logging if requested
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Initialize and run the scraper
        scraper = PlaywrightProductScraper(
            base_url=args.url,
            username=args.username,
            password=args.password,
            headless=args.headless
        )
        
        # Run the scraper and get product data
        products = scraper.run()
        
        # Save products to JSON file
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=2)
        
        logger.info(f"Successfully scraped {len(products)} products and saved to {args.output}")
        
    except Exception as e:
        logger.error(f"An error occurred during scraping: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())