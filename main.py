from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import stripe
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Stripe API key from environment variables
stripe.api_key = os.getenv('STRIPE_API_KEY')

app = Flask(__name__)
YOUR_DOMAIN = 'http://http://127.0.0.1:5000/'

# DB setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'  # Substitute with a secret key of your choice
db = SQLAlchemy(app)

# Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(200), nullable=False)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Create all tables
with app.app_context():
    db.create_all()

def populate_db():
    if Product.query.count() == 0:  # Check if the table is empty and populate it
        products = [
            Product(name='Product 1', price=19.99, description='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.', img_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqknv9bG7lLalT0TE9Bs_VHiWRRIMZONbYew&s'),
            Product(name='Product 2', price=19.99, description='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.', img_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqknv9bG7lLalT0TE9Bs_VHiWRRIMZONbYew&s'),
            Product(name='Product 3', price=19.99, description='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.', img_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqknv9bG7lLalT0TE9Bs_VHiWRRIMZONbYew&s'),
            Product(name='Product 4', price=19.99, description='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.', img_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqknv9bG7lLalT0TE9Bs_VHiWRRIMZONbYew&s'),
            Product(name='Product 5', price=19.99, description='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.', img_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqknv9bG7lLalT0TE9Bs_VHiWRRIMZONbYew&s'),
            Product(name='Product 6', price=19.99, description='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.', img_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqknv9bG7lLalT0TE9Bs_VHiWRRIMZONbYew&s'),
            Product(name='Featured product', price=29.99, description='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.', img_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqknv9bG7lLalT0TE9Bs_VHiWRRIMZONbYew&s')
        ]
        
        db.session.bulk_save_objects(products)
        db.session.commit()
        print("Database popolato con prodotti di esempio!")

with app.app_context():
    populate_db()

@app.route('/')
def home():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/contacts') 
def contacts():
    return render_template('contacts.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        if password == confirm_password:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(name=name, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            message = "User registered successfully!"
            return redirect(url_for('login'))  # Redirect to login page or another appropriate page
        else:
            message = "Passwords do not match!"
    
    return render_template('register.html', message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_name'] = user.name  # Set the user name in the session
            # Login successful
            return redirect(url_for('home'))  # Redirect to home page or another appropriate page
        else:
            message = "Invalid email or password"

    return render_template('login.html', message=message)

@app.context_processor
def inject_user():
    return dict(user_name=session.get('user_name'))

@app.route('/logout')
def logout():
    session.pop('user_name', None)
    return redirect(url_for('home'))

@app.route('/product/<int:id>')
def product(id):
    product = Product.query.get(id)
    return render_template('products.html', product=product)

@app.context_processor
def inject_cart():
    num_items = len(session['cart']) if 'cart' in session else 0
    return {'num_items': num_items}

@app.route('/add_to_cart/<int:id>', methods=['POST'])
def add_to_cart(id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(id)
    session.modified = True
    return redirect(url_for('home'))

@app.route('/cart')
def cart():
    if 'cart' not in session:
        session['cart'] = []
    cart = session['cart']
    products = Product.query.filter(Product.id.in_(cart)).all()
    
    total = round(sum(product.price for product in products), 2)
    
    return render_template('cart.html', products=products, total=total)

@app.route('/remove_from_cart/<int:id>', methods=['POST'])
def remove_from_cart(id):
    session['cart'].remove(id)
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        # Check if the cart is empty
        if 'cart' not in session or not session['cart']:
            return redirect(url_for('cart'))
        
        cart = session['cart']
        products = Product.query.filter(Product.id.in_(cart)).all()

        # Create a list of line items from the cart
        line_items = []
        for product in products:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.name,
                    },
                    'unit_amount': int(product.price * 100),  # Convert the price to cents
                },
                'quantity': cart.count(product.id),
            })

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)


# This route can be called manually to clear the cart for testing purposes
@app.route('/clear_cart')
def clear_cart():
    session['cart'] = []
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
