from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bespoked-sales.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app, origins='http://localhost:3000')

db = SQLAlchemy(app)

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


def calculate_sale_price(product, date):
    discount = Discount.query.filter_by(product_id=product.id).filter(Discount.begin_date <= date, Discount.end_date >= date).first()

    if discount:
        discounted_price = product.purchase_price * (1 - discount.discount_percentage)
        return round(discounted_price, 2)
    else:
        return product.sale_price


@app.route('/salespersons', methods=['GET'])
def list_salespersons():
    salespersons = Salesperson.query.all()
    result = {
        salesperson.id: {
            'id': salesperson.id,
            'first_name': salesperson.first_name,
            'last_name': salesperson.last_name,
            'address': salesperson.address,
            'phone': salesperson.phone,
            'start_date': salesperson.start_date.strftime('%Y-%m-%d') if salesperson.start_date else '',
            'termination_date': salesperson.termination_date.strftime('%Y-%m-%d') if salesperson.termination_date else '',
            'manager': salesperson.manager
        }
        for salesperson in salespersons
    }
    return {"salespersons": result}

@app.route('/update-salesperson', methods=['POST'])
def update_salesperson():
    data = request.get_json()
    data['start_date'] = datetime.strptime(data['start_date'], "%Y-%m-%d").date()
    data['termination_date'] = None if data['termination_date'] == '' else datetime.strptime(data['termination_date'], "%Y-%m-%d").date()
    salesperson = Salesperson.query.get(data['id'])

    existing_salesperson = Salesperson.query.filter_by(first_name=data['first_name'], last_name=data['last_name']).first()
    if existing_salesperson and existing_salesperson.id != salesperson.id:
        return jsonify({"error": "Another salesperson with the same name already exists"}), 400
    
    for key, value in data.items():
        setattr(salesperson, key, value)

    try:
        db.session.commit()
        return jsonify({"message": "Salesperson updated successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update salesperson: {str(e)}"}), 500
    
@app.route('/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    result = {
        product.id: {
            'id': product.id,
            'name': product.name,
            'manufacturer': product.manufacturer,
            'style': product.style,
            'purchase_price': product.purchase_price,
            'sale_price': calculate_sale_price(product, datetime.today().date()),
            'qty_on_hand': product.qty_on_hand,
            'commission_percentage': product.commission_percentage,
        }
        for product in products
    }
    return {"products": result}


@app.route('/update-product', methods=['POST'])
def update_product():
    data = request.get_json()
    product = Product.query.get(data['id'])

    existing_product = Product.query.filter_by(name=data['name']).first()
    if existing_product and existing_product.id != product.id:
        return jsonify({"error": "Another product with the same name already exists"}), 400
    
    for key, value in data.items():
        setattr(product, key, value)

    try:
        db.session.commit()
        return jsonify({"message": "Product updated successfully"})
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": f"Failed to update product: {str(e)}"}), 500


@app.route('/customers', methods=['GET'])
def list_customers():
    customers = Customer.query.all()
    result = {
        customer.id: {
            'id': customer.id,
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'address': customer.address,
            'phone': customer.phone,
            'start_date': customer.start_date.strftime('%Y-%m-%d') if customer.start_date else None,
        }
        for customer in customers
    }
    return {"customers": result}


@app.route('/sales', methods=['GET'])
def list_sales():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
    end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None

    if start_date and end_date:
        sales = Sales.query.filter(Sales.sales_date.between(start_date, end_date)).all()
    else:
        sales = Sales.query.all()

    result = {
        sale.id: {
            'id': sale.id,
            'product': Product.query.get(sale.product_id).name,
            'customer': Customer.query.get(sale.customer_id).first_name + " " + Customer.query.get(sale.customer_id).last_name,
            'sales_date': sale.sales_date.strftime('%Y-%m-%d') if sale.sales_date else None,
            'sale_price': calculate_sale_price(Product.query.get(sale.product_id), sale.sales_date),
            'salesperson': Salesperson.query.get(sale.salesperson_id).first_name + " " + Salesperson.query.get(sale.salesperson_id).last_name,
            'commission_percentage': Product.query.get(sale.product_id).commission_percentage,
        }
        for sale in sales
    }
    return {"sales": result}


@app.route('/create-sale', methods=['POST'])
def create_sale():
    data = request.get_json()

    product = Product.query.get(data['product_id'])

    if product and product.qty_on_hand <= 0:
        return jsonify({"error": f"Failed to create sale: Product is out of stock"}), 400
    
    new_sale = Sales(
        id=len(Sales.query.all()) + 1,
        product_id=data['product_id'],
        salesperson_id=data['salesperson_id'],
        customer_id=data['customer_id'],
        sales_date=None if data['sales_date'] == '' else datetime.strptime(data['sales_date'], "%Y-%m-%d").date(),
    )
    product.qty_on_hand -= 1

    db.session.add(new_sale)

    try:
        db.session.commit()
        return jsonify({"message": "Sale created successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create sale: {str(e)}"}), 500


@app.route('/quarterly-commissions', methods=['GET'])
def quarterly_commission():
    selected_quarter = request.args.get('quarter')

    if selected_quarter == '':
        return {'quarterly_commission': {}}
    
    quarters = {
        'Q1': {'start': datetime(2023, 1, 1), 'end': datetime(2023, 3, 31)},
        'Q2': {'start': datetime(2023, 4, 1), 'end': datetime(2023, 6, 30)},
        'Q3': {'start': datetime(2023, 7, 1), 'end': datetime(2023, 9, 30)},
        'Q4': {'start': datetime(2023, 10, 1), 'end': datetime(2023, 12, 31)},
    }

    start_date = quarters.get(selected_quarter)['start']
    end_date = quarters.get(selected_quarter)['end']

    result = {}

    salespersons = Salesperson.query.all()

    for salesperson in salespersons:
        sales = Sales.query.filter(
            Sales.salesperson_id == salesperson.id,
            Sales.sales_date.between(start_date, end_date)
        ).all()

        total_sales = 0
        total_commission = 0

        for sale in sales:
            total_sales += sale.product.sale_price
            total_commission += sale.product.commission_percentage * sale.product.sale_price

        result[salesperson.id] = {
            'salesperson': f"{salesperson.first_name} {salesperson.last_name}",
            'total_sales': total_sales,
            'total_commission': round(total_commission, 2),
        }

    return {'quarterly_commission': result}



if __name__ == "__main__":
    app.run(debug=True)