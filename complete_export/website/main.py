#!/usr/bin/env python3
"""
Web Application for Product Management

This script runs a Flask web application that serves as a test environment
for the web scraper to extract product data.
"""

from app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)