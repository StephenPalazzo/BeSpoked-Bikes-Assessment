from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)
    manufacturer = db.Column(db.String(100))
    style = db.Column(db.String(50))
    purchase_price = db.Column(db.Float)
    sale_price = db.Column(db.Float)
    qty_on_hand = db.Column(db.Integer)
    commission_percentage = db.Column(db.Float)

class Salesperson(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255))
    phone = db.Column(db.String(20), unique=True)
    start_date = db.Column(db.Date)
    termination_date = db.Column(db.Date)
    manager = db.Column(db.String(100))

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255))
    phone = db.Column(db.String(20), unique=True)
    start_date = db.Column(db.Date)

class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    salesperson_id = db.Column(db.Integer, db.ForeignKey('salesperson.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    sales_date = db.Column(db.Date)
    
    product = db.relationship('Product', backref='sales')
    salesperson = db.relationship('Salesperson', backref='sales')
    customer = db.relationship('Customer', backref='sales')

class Discount(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), unique=True, nullable=False)
    begin_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    discount_percentage = db.Column(db.Float, nullable=False)
    
    product = db.relationship('Product', backref='discounts')

if __name__ == '__main__':

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bespoked-sales.db'
    db.init_app(app)

    with app.app_context():
        db.create_all()

        product1 = Product(
            id = 1,
            name = 'SuperFast',
            manufacturer = 'WeRToys',
            style = 'Racing',
            purchase_price = 100,
            sale_price = 95,
            qty_on_hand = 5,
            commission_percentage = 0.1
        )

        product2 = Product(
            id = 2,
            name = 'SuperCool',
            manufacturer = 'WeRToys',
            style = 'BMX',
            purchase_price = 75,
            sale_price = 75,
            qty_on_hand = 10,
            commission_percentage = 0.05
        )

        salesperson1 = Salesperson(
            id = 1,
            first_name='John',
            last_name='Doe',
            address='123 Main St',
            phone='555-1234',
            start_date=datetime.strptime('2023-01-01', '%Y-%m-%d').date(),
            termination_date=None,
            manager='Jane Manager'
        )

        salesperson2 = Salesperson(
            id = 2,
            first_name='Jim',
            last_name='Bob',
            address='456 Side Way',
            phone='444-6667',
            start_date=datetime.strptime('2022-03-10', '%Y-%m-%d').date(),
            termination_date=None,
            manager='Jane Manager'
        )

        customer1 = Customer(
            id = 1,
            first_name='Alice',
            last_name='Smith',
            address='456 Oak St',
            phone='555-5678',
            start_date=datetime.strptime('2023-01-15', '%Y-%m-%d').date()
        )

        customer2 = Customer(
            id = 2,
            first_name='Bob',
            last_name='Johnson',
            address='789 Pine St',
            phone='555-9876',
            start_date=datetime.strptime('2023-02-20', '%Y-%m-%d').date()
        )

        sale1 = Sales(
            id = 1,
            product=product1,
            salesperson=salesperson1,
            customer=customer1,
            sales_date=datetime.strptime('2023-02-01', '%Y-%m-%d').date()
        )

        sale2 = Sales(
            id = 2,
            product=product2,
            salesperson=salesperson2,
            customer=customer2,
            sales_date=datetime.strptime('2023-03-15', '%Y-%m-%d').date()
        )

        discount1 = Discount(
            id = 1,
            product=product1,
            begin_date=datetime.strptime('2023-12-01', '%Y-%m-%d').date(),
            end_date=datetime.strptime('2024-01-31', '%Y-%m-%d').date(),
            discount_percentage=0.05
        )

        db.session.add_all([product1, product2, salesperson1, salesperson2, customer1, customer2, sale1, sale2, discount1])
        db.session.commit()

    print("Database seeded!")
