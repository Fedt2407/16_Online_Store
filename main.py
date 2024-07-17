from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# DB setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(200), nullable=False)

# Create all tables
with app.app_context():
    db.create_all()

def populate_db():
    if Product.query.count() == 0:  # Popola solo se il database è vuoto
        products = [
            Product(name='Product 1', price=19.99, description='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.', img_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqknv9bG7lLalT0TE9Bs_VHiWRRIMZONbYew&s'),
            Product(name='Product 2', price=19.99, description='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.', img_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqknv9bG7lLalT0TE9Bs_VHiWRRIMZONbYew&s'),
            Product(name='Product 3', price=19.99, description='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.', img_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqknv9bG7lLalT0TE9Bs_VHiWRRIMZONbYew&s'),
            Product(name='Product 4', price=19.99, description='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.', img_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqknv9bG7lLalT0TE9Bs_VHiWRRIMZONbYew&s'),
            Product(name='Product 5', price=19.99, description='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.', img_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqknv9bG7lLalT0TE9Bs_VHiWRRIMZONbYew&s'),
            Product(name='Product 6', price=19.99, description='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.', img_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqknv9bG7lLalT0TE9Bs_VHiWRRIMZONbYew&s')
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

@app.route('/register') 
def register():
    return render_template('register.html')

@app.route('/login') 
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
