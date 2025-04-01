from flask import Flask, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
# Initialize the Flask application
app = Flask(__name__)

# Setup the database URI (SQLite for this example)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the app
db = SQLAlchemy(app)

# Define the Expense model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Expense {self.name} - {self.category} - {self.amount}>"
# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User {self.name} - {self.email}>"

# Route for Register page

# Route for Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Hash the password (no session or flash required)
        hashed_password = generate_password_hash(password)

        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            # Return to the registration page (could add error handling in the frontend)
            return redirect(url_for('register'))

        # Create a new user and add to the database
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Redirect to login page after successful registration
        return redirect(url_for('login'))  # You can define a login page route if needed

    return render_template('register.html')

# Route for Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Fetch user from the database based on email
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            return redirect(url_for('index'))  # Redirect to home page if login successful

        # Return to the login page if credentials don't match (could add error handling here)
        return redirect(url_for('login'))

    return render_template('login.html')


# Home Route
@app.route('/index')
def index():
    expenses = Expense.query.all()
    return render_template('index.html', expenses=expenses)

@app.route('/')
def home():
    return render_template('home.html')






@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Add expense route
@app.route('/add', methods=['POST', 'GET'])
def add_expense():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        amount = float(request.form['amount'])

        # Create a new Expense object and save it to the database
        new_expense = Expense(name=name, category=category, amount=amount)
        db.session.add(new_expense)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_expense.html')

# Route for deleting an expense
@app.route('/delete/<int:id>')
def delete_expense(id):
    expense = Expense.query.get(id)
    if expense:
        db.session.delete(expense)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Create all database tables
    with app.app_context():
        db.create_all()

    app.run(debug=True)
