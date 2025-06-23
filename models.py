from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# ORM setup for Flask application
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    hashed_password = db.Column(db.String, nullable=False)
    mobile = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    security_question_1 = db.Column(db.String, nullable=False)
    security_answer_1 = db.Column(db.String, nullable=False)
    security_question_2 = db.Column(db.String, nullable=False)
    security_answer_2 = db.Column(db.String, nullable=False)
    image_path = db.Column(db.String, nullable=False)
    privilege_id = db.Column(db.Integer, db.ForeignKey('privileges.id'), nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    receipt_id = db.Column(db.String, db.ForeignKey('order_items.receipt_id'), nullable=False)
    address = db.Column(db.String, nullable=False)

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    receipt_id = db.Column(db.String, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    total_item_price = db.Column(db.Float, nullable=False)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String, nullable=False)
