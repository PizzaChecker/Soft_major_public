-- Drop existing tables if they exist
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS privileges;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS order_items;

-- Create the users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE, -- Unique username for each user
    hashed_password TEXT NOT NULL, -- Hashed password for security
    mobile TEXT NOT NULL,
    address TEXT NOT NULL,
    security_question_1 TEXT NOT NULL,
    security_answer_1 TEXT NOT NULL,
    security_question_2 TEXT NOT NULL,
    security_answer_2 TEXT NOT NULL,
    image_path TEXT NOT NULL,
    privilege_id INTEGER NOT NULL, -- Foreign key to privileges table
    FOREIGN KEY (privilege_id) REFERENCES privileges(id) -- Reference to privileges table
);

-- Create the privileges table
CREATE TABLE privileges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    privilege_name TEXT NOT NULL UNIQUE -- Unique name for each privilege
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE, -- Unique name for each product
    description TEXT NOT NULL,
    price REAL NOT NULL CHECK(price > 0), -- Price must be greater than 0
    stock INTEGER NOT NULL CHECK(stock >= 0), -- Stock must be non-negative
    category TEXT NOT NULL -- Category of the product
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL, -- Foreign key to users table
    total_price REAL NOT NULL CHECK(total_price > 0), -- Total price must be greater than 0
    order_date TEXT NOT NULL, -- Date of the order
    status TEXT NOT NULL CHECK(status IN ('pending', 'shipped', 'delivered', 'cancelled')), -- Order status
    receipt_id TEXT NOT NULL, -- Receipt for the order
    address TEXT NOT NULL, -- Address for delivery
    FOREIGN KEY (user_id) REFERENCES users(id), -- Reference to users table
    FOREIGN KEY (receipt_id) REFERENCES order_items(receipt_id)
);

CREATE TABLE order_items (
    receipt_id TEXT NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    price REAL NOT NULL CHECK(price > 0),
    total_item_price REAL NOT NULL CHECK(total_item_price > 0), -- Total price for this item (quantity * price)
    PRIMARY KEY (receipt_id, product_id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

INSERT INTO privileges (privilege_name)
VALUES 
('user'),
('admin');