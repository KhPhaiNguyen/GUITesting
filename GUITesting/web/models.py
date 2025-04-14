from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'Products'  # Đặt tên bảng
    productID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    productionInfo = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)

    specifications = db.relationship('ProductSpecification', backref='product', lazy=True)

class ProductSpecification(db.Model):
    __tablename__ = 'ProductSpecifications'
    specID = db.Column(db.Integer, primary_key=True)
    productID = db.Column(db.Integer, db.ForeignKey('Products.productID'))
    processor = db.Column(db.String(100), nullable=False)
    graphics = db.Column(db.String(100), nullable=False)
    ram = db.Column(db.String(50), nullable=False)
    storage = db.Column(db.String(50), nullable=False)
    screen = db.Column(db.String(50), nullable=False)
    sound = db.Column(db.String(50), nullable=False)
    ports = db.Column(db.String(50), nullable=False)
    dimensions = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.String(50), nullable=False)
    additionalFeatures = db.Column(db.String(200), nullable=True)
    utilities = db.Column(db.String(200), nullable=True)
    batteryAndCharging = db.Column(db.String(200), nullable=True)


class User(UserMixin, db.Model):
    __tablename__ = 'Users'

    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    fullname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def get_id(self):
        # Trả về userID như một chuỗi
        return str(self.userID)


class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('Users.userID'))  # Sửa khóa ngoại trỏ đến Users.userID
    user = db.relationship('User', backref='carts', lazy=True)  # Mối quan hệ

class CartItem(db.Model):
    __tablename__ = 'cart_item'
    id = db.Column(db.Integer, primary_key=True)
    cartID = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    productID = db.Column(db.Integer, db.ForeignKey('Products.productID'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    product = db.relationship('Product', backref='cart_items')
    cart = db.relationship('Cart', backref='items', lazy=True)  # Thêm mối quan hệ này


