from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
from werkzeug.security import generate_password_hash, check_password_hash
import json

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# Demo user
DEMO_USER = {
    "username": "demo",
    "password": generate_password_hash("password123")
}

# Demo product data
PRODUCTS = [
    {"id": 1, "name": "Laptop", "category": "Electronics", "price": 999.99, "stock": 50},
    {"id": 2, "name": "Smartphone", "category": "Electronics", "price": 699.99, "stock": 100},
    {"id": 3, "name": "Headphones", "category": "Accessories", "price": 159.99, "stock": 200},
    {"id": 4, "name": "Monitor", "category": "Electronics", "price": 299.99, "stock": 30},
    {"id": 5, "name": "Keyboard", "category": "Accessories", "price": 89.99, "stock": 150},
    {"id": 6, "name": "Mouse", "category": "Accessories", "price": 49.99, "stock": 200},
    {"id": 7, "name": "Tablet", "category": "Electronics", "price": 399.99, "stock": 75},
    {"id": 8, "name": "Webcam", "category": "Accessories", "price": 79.99, "stock": 120},
    {"id": 9, "name": "Router", "category": "Networking", "price": 129.99, "stock": 45},
    {"id": 10, "name": "External Drive", "category": "Storage", "price": 149.99, "stock": 60},
    {"id": 11, "name": "Printer", "category": "Office", "price": 249.99, "stock": 25},
    {"id": 12, "name": "Speaker", "category": "Audio", "price": 199.99, "stock": 40},
]

# Routes
@app.route('/')
def home():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == DEMO_USER['username'] and check_password_hash(DEMO_USER['password'], password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/menu')
def menu():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('menu.html')

@app.route('/data-management')
def data_management():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('data_management.html')

@app.route('/inventory')
def inventory():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('inventory.html')

@app.route('/products')
def products():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Get page number from query parameter, default to 1
    page = request.args.get('page', 1, type=int)
    per_page = 5  # 5 products per page
    
    # Calculate start and end indices for pagination
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    # Get products for current page
    products_page = PRODUCTS[start_idx:end_idx]
    total_pages = (len(PRODUCTS) + per_page - 1) // per_page
    
    return render_template('products.html', 
                          products=products_page, 
                          page=page, 
                          total_pages=total_pages)

# API endpoint for fetching products
@app.route('/api/products')
def api_products():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    page = request.args.get('page', 1, type=int)
    per_page = 5
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    products_page = PRODUCTS[start_idx:end_idx]
    total_pages = (len(PRODUCTS) + per_page - 1) // per_page
    
    return jsonify({
        "products": products_page,
        "page": page,
        "total_pages": total_pages
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)