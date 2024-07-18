from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# DB setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        if password == confirm_password:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(email=email, password=hashed_password)
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
            # Login successful
            return redirect(url_for('home'))  # Redirect to home page or another appropriate page
        else:
            message = "Invalid email or password"

    return render_template('login.html', message=message)

@app.route('/product/<int:id>')
def product(id):
    product = Product.query.get(id)
    return render_template('products.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)
