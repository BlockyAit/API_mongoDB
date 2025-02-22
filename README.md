# API_mongoDB

# Computer Peripherals Store - Backend

## Overview
This project is a backend system for a **Computer Peripherals Store** that provides a REST API for managing products, users, and orders. It includes **web scraping**, **MongoDB integration**, **authentication (JWT)**, and **deployment readiness**.

## Features
- **Web Scraping**: Scrapes product data from an external website and stores it in MongoDB.
- **User Authentication**: JWT-based authentication with role-based access control.
- **CRUD Operations**: Supports Create, Read, Update, and Delete operations for Products, Users, and Orders.
- **Query Optimization**: Uses indexing for efficient queries.

---

## Tech Stack
- **Python** (Flask / FastAPI)
- **MongoDB** (NoSQL database)
- **BeautifulSoup** (Web Scraping)
- **JWT** (Authentication)

---

## Installation & Setup

### 1. Clone the Repository
```sh
 git clone https://github.com/BlockyAit/API_mongoDB.git
 cd computer-peripherals-store
```

### 2. Install Dependencies


### 3. Setup Environment Variables
Create a `.env` file in the root directory:
```env
MONGO_URI=mongodb://localhost:27017/computer_peripherals_store
SECRET_KEY=your_secret_key
```

### 4. Run the Server
```sh
 python app.py
```

### 5. Test API with Postman or cURL
```sh
 curl -X GET http://localhost:5000/products
```

---

## API Endpoints

### **Authentication**
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/register` | Register a new user |
| POST | `/login` | Login and get JWT token |

### **Products**
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/products` | Get all products |
| GET | `/products/<id>` | Get a product by ID |
| POST | `/products` | Add a new product (Admin only) |
| PUT | `/products/<id>` | Update product (Admin only) |
| DELETE | `/products/<id>` | Delete product (Admin only) |

### **Orders**
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/orders` | Get all orders |
| POST | `/orders` | Create an order |

---


## Contributing
Feel free to submit pull requests and issues. Contributions are welcome!

---

