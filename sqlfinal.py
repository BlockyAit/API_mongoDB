from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/computer_peripherals_store"
mongo = PyMongo(app)

# Secret Key for JWT
SECRET_KEY = "your_secret_key"

# Middleware for Token Authentication
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = mongo.db.users.find_one({"username": data["username"]})
            if not current_user:
                return jsonify({'message': 'User not found!'}), 401
        except:
            return jsonify({'message': 'Invalid token!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# Route: User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    
    if mongo.db.users.find_one({"username": username}):
        return jsonify({"message": "User already exists!"}), 400

    hashed_password = generate_password_hash(password)
    mongo.db.users.insert_one({"username": username, "password": hashed_password, "role": "user"})
    
    return jsonify({"message": "User registered successfully!"})

# Route: User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    
    user = mongo.db.users.find_one({"username": username})
    if not user or not check_password_hash(user['password'], password):
        return jsonify({"message": "Invalid credentials!"}), 401

    token = jwt.encode({"username": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, SECRET_KEY, algorithm="HS256")
    return jsonify({"token": token})

# Middleware for Admin Access
def admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user["role"] != "admin":
            return jsonify({"message": "Admin access required!"}), 403
        return f(current_user, *args, **kwargs)
    return decorated

# Route: Add Product (Admin Only)
@app.route('/products', methods=['POST'])
@token_required
@admin_required
def add_product(current_user):
    data = request.json
    mongo.db.products.insert_one(data)
    return jsonify({"message": "Product added!"})

# Route: Get All Products
@app.route('/products', methods=['GET'])
def get_products():
    products = list(mongo.db.products.find({}, {"_id": 0}))
    return jsonify(products)

# Route: Update Product (Admin Only)
@app.route('/products/<product_id>', methods=['PUT'])
@token_required
@admin_required
def update_product(current_user, product_id):
    data = request.json
    mongo.db.products.update_one({"id_": product_id}, {"$set": data})
    return jsonify({"message": "Product updated!"})

# Route: Delete Product (Admin Only)
@app.route('/products/<product_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_product(current_user, product_id):
    mongo.db.products.delete_one({"id_": product_id})
    return jsonify({"message": "Product deleted!"})

# Route: Place an Order (User Only)
@app.route('/orders', methods=['POST'])
@token_required
def place_order(current_user):
    data = request.json
    order = {
        "user_id": current_user["username"],
        "products": data["products"],
        "timestamp": datetime.datetime.utcnow()
    }
    mongo.db.orders.insert_one(order)
    return jsonify({"message": "Order placed successfully!"})

# Route: Get User Orders
@app.route('/orders', methods=['GET'])
@token_required
def get_orders(current_user):
    orders = list(mongo.db.orders.find({"user_id": current_user["username"]}, {"_id": 0}))
    return jsonify(orders)

# Web Scraping Function
def scrape_products():
    url = "https://twen.rs-online.com/web/c/computing-peripherals/"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    products = []
    
    product_grid = soup.find('div', {'class': '-mx-2 flex flex-wrap'})
    if not product_grid:
        return []

    for product_card in product_grid.find_all('div', {'class': 'flex w-full flex-col p-2 md:w-1/2 lg:w-1/3'}):
        try:
            name = product_card.find('div', {'class': 'src__LineClampGrid-sc-1r3bpf8-5 kAwYla'}).text.strip()
            price = product_card.find('div', {'class': 'sc-aXZVg bZfWPp'}).text.strip()
            link = product_card.find('a', {'class': 'sc-aXZVg dyjyw'})['href']
            products.append({"name": name, "price": price, "link": link})
        except:
            continue

    return products

# Route: Scrape and Save Products (Admin Only)
@app.route('/scrape', methods=['GET'])
@token_required
@admin_required
def scrape_and_save(current_user):
    products = scrape_products()
    if products:
        mongo.db.products.insert_many(products)
        return jsonify({"message": "Products scraped and saved!"})
    return jsonify({"message": "No products found!"})

# Start Flask Server
if __name__ == '__main__':
    app.run(debug=True)
